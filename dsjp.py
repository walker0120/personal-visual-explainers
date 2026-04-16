"""
厚生労働省「医療用医薬品供給状況」Excelを使った供給状況取得モジュール
毎日更新される公式データを無料で利用する
"""

import hashlib
import requests
import io
import threading
from datetime import datetime, date, timedelta
from bs4 import BeautifulSoup
import pandas as pd

MHLW_PAGE_URL = "https://www.mhlw.go.jp/stf/seisakunitsuite/bunya/kenkou_iryou/iryou/kouhatu-iyaku/04_00003.html"
MHLW_BASE_URL = "https://www.mhlw.go.jp"

STATUS_EMOJI = {
    "通常出荷": "🟢",
    "限定出荷": "🟡",
    "供給停止": "🔴",
    "販売中止": "⛔",
}

# Excelデータキャッシュ（メモリ内）
_cache = {
    "df": None,
    "loaded_at": None,
    "excel_hash": None,
    "col_map": None,  # 動的に検出した列インデックス
}
_cache_lock = threading.Lock()
CACHE_TTL_HOURS = 6
MAX_MSG_CHARS = 4500  # LINEメッセージ1件あたりの文字数上限（余裕を持って設定）

# 列インデックスのデフォルト（フォールバック用）
# 厚労省Excelの実際の列構造（2025年版）に基づく
_COL_DEFAULTS = {
    "ingredient": 2,   # ③成分名
    "name":       5,   # ⑥品名（承認書に記載の正式名称）
    "dosage":     3,   # ④規格単位
    "maker":      6,   # ⑦製造販売業者名
    "target":     11,  # ⑫出荷対応の状況
    "status":     11,  # ⑫出荷対応の状況（①通常出荷/②限定出荷/③供給停止）
    "new_flag":   20,  # 今回掲載時の更新有無（Newと表示される列）
}

# 各フィールドを列名から特定するためのキーワード
_COL_KEYWORDS = {
    "ingredient": ["成分名"],
    "name":       ["品名"],          # 「品目名」ではなく「品名」
    "dosage":     ["規格"],
    "maker":      ["製造販売業者名"],  # 「製造販売業者の〜」列と区別するため「名」まで含める
    "target":     ["出荷対応"],
    "status":     ["出荷対応"],
    "new_flag":   ["更新有無"],       # 今回掲載時の更新有無
}


def _detect_columns(df) -> dict:
    """DataFrame のヘッダー名を走査して列インデックスを動的に検出する。
    見つからない列はデフォルト値（固定インデックス）を使う。"""
    col_map = dict(_COL_DEFAULTS)
    for i, col in enumerate(df.columns):
        col_str = str(col)
        for field, keywords in _COL_KEYWORDS.items():
            if any(kw in col_str for kw in keywords):
                col_map[field] = i
                break
    print(f"[MHLW] 列マッピング: {col_map}")
    return col_map


def get_status_emoji(status: str) -> str:
    if not isinstance(status, str):
        return "🟢"
    for key, emoji in STATUS_EMOJI.items():
        if key in status:
            return emoji
    return "🟡"


def _fetch_excel_url() -> str:
    """MHLWのページから最新Excelファイルのダウンロードリンクを取得する"""
    try:
        resp = requests.get(MHLW_PAGE_URL, timeout=15)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")
        for link in soup.find_all("a", href=True):
            href = link["href"]
            if "iyakuhinkyoukyu.xlsx" in href or "kyoukyu.xlsx" in href:
                if href.startswith("http"):
                    return href
                return MHLW_BASE_URL + href
    except Exception as e:
        print(f"[MHLW] Excelリンク取得失敗: {e}")
    # フォールバック：今日の日付でURLを組み立て
    today = date.today()
    yy = str(today.year)[2:]
    mm = str(today.month).zfill(2)
    dd = str(today.day).zfill(2)
    return f"{MHLW_BASE_URL}/content/10800000/{yy}{mm}{dd}iyakuhinkyoukyu.xlsx"


def _load_excel_bytes() -> tuple:
    """ExcelをDLしてDataFrameとMD5ハッシュを返す"""
    url = _fetch_excel_url()
    print(f"[MHLW] Excelダウンロード中: {url}")
    resp = requests.get(url, timeout=30)
    resp.raise_for_status()
    content = resp.content
    excel_hash = hashlib.md5(content).hexdigest()
    df = pd.read_excel(io.BytesIO(content), header=1)
    print(f"[MHLW] 読み込み完了: {len(df)}行 hash={excel_hash[:8]}")
    return df, excel_hash


def _get_df() -> pd.DataFrame:
    """キャッシュ付きでDataFrameを取得する"""
    with _cache_lock:
        now = datetime.now()
        if (
            _cache["df"] is not None
            and _cache["loaded_at"] is not None
            and (now - _cache["loaded_at"]) <= timedelta(hours=CACHE_TTL_HOURS)
        ):
            return _cache["df"]

    # キャッシュ期限切れ → 再取得（ロック外でネットワークI/O）
    try:
        new_df, new_hash = _load_excel_bytes()
        new_col_map = _detect_columns(new_df)
        with _cache_lock:
            _cache["df"] = new_df
            _cache["loaded_at"] = datetime.now()
            _cache["excel_hash"] = new_hash
            _cache["col_map"] = new_col_map
        return new_df
    except Exception as e:
        print(f"[MHLW] Excel取得エラー: {e}")
        with _cache_lock:
            return _cache["df"] if _cache["df"] is not None else pd.DataFrame()


def _get_col_map() -> dict:
    """キャッシュ済みの列マッピングを返す。未取得ならデフォルトを返す。"""
    with _cache_lock:
        return _cache["col_map"] if _cache["col_map"] is not None else dict(_COL_DEFAULTS)


def _parse_row(row) -> dict:
    """DataFrameの1行から必要情報を抽出する"""
    def safe(val):
        if pd.isna(val):
            return ""
        return str(val).strip()

    cm = _get_col_map()
    return {
        "ingredient": safe(row.iloc[cm["ingredient"]]),
        "name":       safe(row.iloc[cm["name"]]),
        "dosage":     safe(row.iloc[cm["dosage"]]),
        "maker":      safe(row.iloc[cm["maker"]]),
        "target":     safe(row.iloc[cm["target"]]),
        "status":     safe(row.iloc[cm["status"]]),
    }


def _to_katakana(text: str) -> str:
    """ひらがなをカタカナに変換（例：おーぐめんちん → オーグメンチン）"""
    return "".join(
        chr(ord(c) + 0x60) if "\u3041" <= c <= "\u3096" else c
        for c in text
    )


def search_drug(keyword: str) -> list:
    """品名または一般名でキーワード検索して供給状況リストを返す"""
    df = _get_df()
    if df.empty:
        return []

    cm = _get_col_map()
    col_name       = df.iloc[:, cm["name"]].astype(str)        # 品目名（販売名）
    col_ingredient = df.iloc[:, cm["ingredient"]].astype(str)  # 成分名（一般名）

    def _contains(col, kw):
        return col.str.contains(kw, na=False, case=False, regex=False)

    mask = _contains(col_name, keyword) | _contains(col_ingredient, keyword)

    # ひらがな入力の場合はカタカナ変換版でも追加検索
    keyword_kata = _to_katakana(keyword)
    if keyword_kata != keyword:
        mask |= _contains(col_name, keyword_kata) | _contains(col_ingredient, keyword_kata)

    matched = df[mask]

    results = []
    for _, row in matched.iterrows():
        item = _parse_row(row)
        if item["name"]:
            results.append(item)

    return results


# ── 差分検知 ────────────────────────────────────────

def _compute_diff(prev_df, new_df) -> dict:
    """2つのDataFrameを比較して差分（新規・変化・回復）を返す"""
    def to_item_dict(df):
        if df is None or df.empty:
            return {}
        d = {}
        for _, row in df.iterrows():
            item = _parse_row(row)
            if item["name"]:
                key = f"{item['name']}||{item['dosage']}||{item['maker']}"
                d[key] = item
        return d

    prev = to_item_dict(prev_df)
    new = to_item_dict(new_df)

    added = []      # 新規追加（通常出荷以外）
    changed = []    # ステータス変化
    recovered = []  # 出荷調整解除（リストから削除 or 通常出荷に戻った）

    for key, item in new.items():
        if key not in prev:
            if "通常出荷" not in (item["status"] or ""):
                added.append(item)
        elif prev[key]["status"] != item["status"]:
            changed.append({
                "item": item,
                "old_status": prev[key]["status"],
                "new_status": item["status"],
            })

    for key, item in prev.items():
        if key not in new and "通常出荷" not in (item["status"] or ""):
            recovered.append(item)

    return {"added": added, "changed": changed, "recovered": recovered}


def get_diff_updates() -> dict:
    """前回からの差分を返す。変化なければ全キーが空リスト。"""
    # ロック外でネットワークI/O
    try:
        new_df, new_hash = _load_excel_bytes()
    except Exception as e:
        print(f"[MHLW] 更新チェック失敗: {e}")
        return {"added": [], "changed": [], "recovered": []}

    with _cache_lock:
        old_hash = _cache.get("excel_hash")
        old_df = _cache["df"]

        # ハッシュが一致 → 変化なし
        if new_hash == old_hash and old_df is not None:
            print(f"[MHLW] 変化なし (hash={new_hash[:8]})")
            return {"added": [], "changed": [], "recovered": []}

        diff = _compute_diff(old_df, new_df)
        _cache["df"] = new_df
        _cache["loaded_at"] = datetime.now()
        _cache["excel_hash"] = new_hash

    return diff


def get_new_items() -> list:
    """今回の更新でNewがついた品目一覧を返す（「最新」コマンド用）"""
    df = _get_df()
    if df.empty:
        return []

    cm = _get_col_map()
    new_flag_col = cm.get("new_flag", 20)
    col_flag = df.iloc[:, new_flag_col].astype(str)
    mask = col_flag.str.contains("New", na=False, case=False, regex=False)
    new_rows = df[mask]

    results = []
    for _, row in new_rows.iterrows():
        item = _parse_row(row)
        if item["name"]:
            results.append(item)

    return results


def format_new_items(items: list) -> list:
    """最新更新品目をLINEメッセージ用にフォーマット。list[str]を返す"""
    today_str = date.today().strftime("%Y/%m/%d")

    if not items:
        return [
            f"📋 最新の更新情報（{today_str}現在）\n"
            "━━━━━━━━━━━━━━━\n"
            "現在、新着の更新情報はありません。\n"
            "出典：厚生労働省"
        ]

    item_blocks = [_build_item_block(item) for item in items]
    header_template = f"📋 最新の更新情報{{page_label}}（{today_str}現在）\n━━━━━━━━━━━━━━━"
    footer = "\n\n━━━━━━━━━━━━━━━\n出典：厚生労働省"

    return _split_into_pages(item_blocks, header_template, footer)


def get_update_history(limit: int = 50) -> list:
    """通常出荷以外の品目一覧を返す（手動確認コマンド用）"""
    df = _get_df()
    if df.empty:
        return []

    cm = _get_col_map()
    col_status = df.iloc[:, cm["status"]].astype(str)
    # 通常出荷以外（限定出荷・供給停止など）の品目を抽出
    mask = ~col_status.str.contains("通常出荷", na=False)
    problems = df[mask].head(limit)

    results = []
    for _, row in problems.iterrows():
        item = _parse_row(row)
        if item["name"]:
            results.append(item)

    return results


# ── フォーマット関数 ────────────────────────────────

def _normalize_status(status: str) -> str:
    """ステータスから括弧内の補足情報（自社事情など）を除去して主区分だけ返す"""
    import re
    return re.sub(r"[（(][^）)]*[）)]", "", status).strip()


def _build_item_block(item: dict) -> str:
    """1品目のテキストブロックを生成する"""
    status_raw = item["status"] or ""
    status_short = _normalize_status(status_raw)
    emoji = get_status_emoji(status_short)
    name_part = item["name"]
    if item["dosage"]:
        name_part += f" {item['dosage']}"
    lines = [f"\n{emoji} {name_part}"]
    if item["maker"]:
        lines.append(f"　{item['maker']}")
    if status_short:
        lines.append(f"　→ {status_short}")
    return "\n".join(lines)


def _split_into_pages(item_blocks: list, header_template: str, footer: str) -> list:
    """品目ブロックのリストを4500文字制限でページ分割してメッセージリストを返す"""
    pages = []
    current_page = []
    current_len = 0

    for block in item_blocks:
        if current_len + len(block) > MAX_MSG_CHARS and current_page:
            pages.append(current_page)
            current_page = [block]
            current_len = len(block)
        else:
            current_page.append(block)
            current_len += len(block)
    if current_page:
        pages.append(current_page)

    total = len(pages)
    messages = []
    for i, page in enumerate(pages, 1):
        page_label = f" ({i}/{total})" if total > 1 else ""
        header = header_template.format(page_label=page_label)
        body = "".join(page)
        if i == total:
            messages.append(header + body + footer)
        else:
            messages.append(header + body)

    return messages


def format_search_result(keyword: str, results: list) -> list:
    """検索結果をLINEメッセージ用にフォーマット。list[str]を返す（複数メッセージ対応）"""
    if not results:
        return [
            f"🔍 「{keyword}」の検索結果\n"
            "━━━━━━━━━━━━━━━\n"
            "厚労省の医薬品供給状況リストに\n"
            "見つかりませんでした。\n\n"
            "別の表記や成分名（一般名）でも\n"
            "検索してみてください。\n"
            f"詳細 → {MHLW_PAGE_URL}"
        ]

    # 問題あり（通常出荷以外）を先頭に
    problems = [r for r in results if "通常出荷" not in r["status"]]
    normals = [r for r in results if "通常出荷" in r["status"]]
    sorted_results = problems + normals

    item_blocks = [_build_item_block(item) for item in sorted_results]
    today_str = date.today().strftime("%Y/%m/%d")
    header_template = f"🔍 「{keyword}」の検索結果{{page_label}}\n━━━━━━━━━━━━━━━"
    footer = (
        f"\n\n━━━━━━━━━━━━━━━\n"
        f"出典：厚生労働省（{today_str}現在）\n"
        "※通常出荷でも実際の入手状況が\n"
        "　異なる場合があります"
    )

    return _split_into_pages(item_blocks, header_template, footer)


def format_diff_notification(diff: dict) -> list:
    """差分通知をLINEメッセージ用にフォーマット。list[str]を返す"""
    added = diff.get("added", [])
    changed = diff.get("changed", [])
    recovered = diff.get("recovered", [])

    if not added and not changed and not recovered:
        return []

    now_str = datetime.now().strftime("%Y/%m/%d %H:%M")
    lines = [
        f"📢 厚労省リスト更新（{now_str}）",
        "━━━━━━━━━━━━━━━",
    ]

    if added:
        lines.append(f"\n【新たに出荷調整（{len(added)}件）】")
        for item in added:
            st = _normalize_status(item["status"] or "")
            emoji = get_status_emoji(st)
            name = item["name"]
            if item["dosage"]:
                name += f" {item['dosage']}"
            lines.append(f"{emoji} {name}")
            if item["maker"]:
                lines.append(f"　{item['maker']}")
            if st:
                lines.append(f"　→ {st}")

    if changed:
        lines.append(f"\n【ステータス変化（{len(changed)}件）】")
        for entry in changed:
            item = entry["item"]
            new_st = _normalize_status(entry["new_status"] or "")
            old_st = _normalize_status(entry["old_status"] or "")
            emoji = get_status_emoji(new_st)
            name = item["name"]
            if item["dosage"]:
                name += f" {item['dosage']}"
            lines.append(f"{emoji} {name}")
            if item["maker"]:
                lines.append(f"　{item['maker']}")
            lines.append(f"　{old_st} → {new_st}")

    if recovered:
        lines.append(f"\n【出荷調整解除（{len(recovered)}件）】")
        for item in recovered:
            name = item["name"]
            if item["dosage"]:
                name += f" {item['dosage']}"
            lines.append(f"🟢 {name}")
            if item["maker"]:
                lines.append(f"　{item['maker']}")

    lines.append("\n━━━━━━━━━━━━━━━")
    lines.append("出典：厚生労働省")

    # 4500文字超えなら行単位で分割
    full_text = "\n".join(lines)
    if len(full_text) <= MAX_MSG_CHARS:
        return [full_text]

    messages = []
    current_lines = []
    current_len = 0
    for line in lines:
        line_len = len(line) + 1  # +1 for newline
        if current_len + line_len > MAX_MSG_CHARS and current_lines:
            messages.append("\n".join(current_lines))
            current_lines = [line]
            current_len = line_len
        else:
            current_lines.append(line)
            current_len += line_len
    if current_lines:
        messages.append("\n".join(current_lines))

    return messages


def format_daily_update(updates: list, target_date: str = None) -> str:
    """問題あり品目の一覧をLINEメッセージ用にフォーマット（手動確認コマンド用）"""
    if not target_date:
        target_date = date.today().strftime("%Y/%m/%d")

    if not updates:
        return (
            f"【📋 {target_date} の出荷調整情報】\n"
            "━━━━━━━━━━━━━━━\n"
            "現在、出荷調整中の品目はありません。\n"
            "出典：厚生労働省"
        )

    grouped: dict = {}
    for item in updates:
        status = item["status"] or "不明"
        grouped.setdefault(status, []).append(item)

    lines = [
        f"【📋 {target_date} の出荷調整情報】",
        "━━━━━━━━━━━━━━━",
    ]

    for status, items in grouped.items():
        emoji = get_status_emoji(status)
        lines.append(f"\n{emoji} {status}（{len(items)}件）")
        for item in items[:5]:
            name = item["name"]
            if item["dosage"]:
                name += f" {item['dosage']}"
            lines.append(f"　・{name}")
            if item["maker"]:
                lines.append(f"　　{item['maker']}")
        if len(items) > 5:
            lines.append(f"　　他 {len(items) - 5} 件")

    lines.append("\n━━━━━━━━━━━━━━━")
    lines.append("出典：厚生労働省")

    return "\n".join(lines)
