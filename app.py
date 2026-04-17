"""
DSJP LINE Bot - メインアプリケーション

機能:
  1. 薬名をLINEに送信 → DSJPから供給状況を検索して返答
  2. 厚労省Excelが更新されたら差分をプッシュ通知（6時間ごとにチェック）
"""

import os
import logging
from datetime import datetime

from flask import Flask, request, abort, jsonify
from linebot.v3 import WebhookHandler
from linebot.v3.exceptions import InvalidSignatureError
from linebot.v3.messaging import (
    ApiClient,
    Configuration,
    MessagingApi,
    ReplyMessageRequest,
    PushMessageRequest,
    TextMessage,
)
from linebot.v3.webhooks import MessageEvent, TextMessageContent
from apscheduler.schedulers.background import BackgroundScheduler
import pytz

import dsjp
import favorites

# ── ログ設定 ──────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger(__name__)

# ── Flask & LINE 設定 ──────────────────────────────
app = Flask(__name__)

LINE_CHANNEL_SECRET = os.environ["LINE_CHANNEL_SECRET"]
LINE_CHANNEL_ACCESS_TOKEN = os.environ["LINE_CHANNEL_ACCESS_TOKEN"]
MY_LINE_USER_ID = os.environ["MY_LINE_USER_ID"]

configuration = Configuration(access_token=LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)


def get_messaging_api() -> MessagingApi:
    return MessagingApi(ApiClient(configuration))


# ── Webhookエンドポイント ──────────────────────────
@app.route("/callback", methods=["POST"])
def callback():
    signature = request.headers.get("X-Line-Signature", "")
    body = request.get_data(as_text=True)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        logger.warning("無効な署名")
        abort(400)

    return "OK"


@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event: MessageEvent):
    """ユーザーからのメッセージを処理"""
    user_text = event.message.text.strip()
    reply_token = event.reply_token
    user_id = event.source.user_id

    logger.info(f"受信メッセージ: {user_text}")

    api = get_messaging_api()

    if user_text in ("ヘルプ", "help", "？", "?"):
        api.reply_message(ReplyMessageRequest(
            reply_token=reply_token,
            messages=[TextMessage(text=build_help_message())],
        ))
        return

    if user_text == "お気に入り":
        api.reply_message(ReplyMessageRequest(
            reply_token=reply_token,
            messages=[TextMessage(text="📋 取得中...")],
        ))
        def _list_and_push():
            try:
                msg = build_favorites_list(user_id)
                get_messaging_api().push_message(PushMessageRequest(
                    to=user_id,
                    messages=[TextMessage(text=msg)],
                ))
            except Exception as e:
                logger.error(f"お気に入り一覧pushエラー: {e}")
        import threading
        threading.Thread(target=_list_and_push, daemon=True).start()
        return

    if user_text.startswith("登録 "):
        drug_name = user_text[3:].strip()
        if drug_name:
            msg = favorites.add_favorite(user_id, drug_name)
        else:
            msg = "登録する薬の名前を入力してください。\n例：登録 オーグメンチン"
        api.reply_message(ReplyMessageRequest(
            reply_token=reply_token,
            messages=[TextMessage(text=msg)],
        ))
        return

    if user_text.startswith("削除 "):
        drug_name = user_text[3:].strip()
        if drug_name:
            msg = favorites.remove_favorite(user_id, drug_name)
        else:
            msg = "削除する薬の名前を入力してください。\n例：削除 オーグメンチン"
        api.reply_message(ReplyMessageRequest(
            reply_token=reply_token,
            messages=[TextMessage(text=msg)],
        ))
        return

    # 検索・更新はExcel読み込みで時間がかかる場合があるため
    # 「検索中...」を即時返信したあとバックグラウンドで検索しpushで送信する
    api.reply_message(ReplyMessageRequest(
        reply_token=reply_token,
        messages=[TextMessage(text="🔍 検索中...")],
    ))

    def _search_and_push():
        try:
            if user_text in ("今日の情報", "新着", "更新"):
                texts = [fetch_daily_update()]
            elif user_text == "最新":
                texts = fetch_new_items()
            else:
                texts = fetch_drug_search(user_text)
            push_api = get_messaging_api()
            for t in texts[:5]:
                push_api.push_message(PushMessageRequest(
                    to=user_id,
                    messages=[TextMessage(text=t)],
                ))
        except Exception as e:
            logger.error(f"検索pushエラー: {e}")

    import threading
    threading.Thread(target=_search_and_push, daemon=True).start()


def fetch_drug_search(keyword: str) -> list:
    """薬名検索して結果テキストのリストを返す"""
    logger.info(f"DSJP検索: {keyword}")
    results = dsjp.search_drug(keyword)
    return dsjp.format_search_result(keyword, results)


def fetch_new_items() -> list:
    """最新更新（Newフラグあり）品目を取得してフォーマット"""
    logger.info("最新更新品目を取得中...")
    items = dsjp.get_new_items()
    return dsjp.format_new_items(items)


def fetch_daily_update() -> str:
    """本日の出荷調整品目一覧を取得してフォーマット"""
    logger.info("更新履歴を取得中...")
    updates = dsjp.get_update_history(limit=30)
    return dsjp.format_daily_update(updates)


def build_favorites_list(user_id: str) -> str:
    """お気に入り一覧と現在のステータスをまとめたメッセージを返す"""
    items = favorites.list_favorites(user_id)
    if not items:
        return (
            "⭐ お気に入り一覧\n"
            "━━━━━━━━━━━━━━━\n"
            "まだ登録されていません。\n\n"
            "登録方法：\n"
            "　登録 オーグメンチン"
        )

    lines = ["⭐ お気に入り一覧", "━━━━━━━━━━━━━━━"]
    for item in items:
        drug = item["drug_name"]
        status = item["last_status"] or "未取得"
        lines.append(f"💊 {drug}\n   {status}")
    lines.append("━━━━━━━━━━━━━━━")
    lines.append("削除：削除 薬品名")
    return "\n".join(lines)


def build_help_message() -> str:
    return (
        "💊 DSJP出荷調整ボット\n"
        "━━━━━━━━━━━━━━━\n"
        "【使い方】\n"
        "薬の品名を送ると供給状況を調べます。\n\n"
        "例：\n"
        "　ノルバスク\n"
        "　オーグメンチン\n"
        "　ランソプラゾール\n\n"
        "※一般名（成分名）でも検索できます\n"
        "　例：アムロジピン、アモキシシリン\n\n"
        "【コマンド】\n"
        "　「最新」→ 今回の新着更新品目\n"
        "　「今日の情報」→ 出荷調整中の品目一覧\n"
        "　「お気に入り」→ 登録薬の一覧と現在のステータス\n"
        "　「登録 薬品名」→ お気に入りに追加\n"
        "　「削除 薬品名」→ お気に入りから削除\n"
        "　「ヘルプ」→ この画面\n"
        "━━━━━━━━━━━━━━━\n"
        "厚労省リスト更新時に自動通知します"
    )


# ── 更新検知プッシュ通知 ───────────────────────────
def check_and_notify():
    """厚労省Excelの差分をチェックし、変化があればプッシュ通知"""
    logger.info("更新チェック中...")
    try:
        diff = dsjp.get_diff_updates()
        if not diff["added"] and not diff["changed"] and not diff["recovered"]:
            logger.info("変化なし: 通知スキップ")
        else:
            texts = dsjp.format_diff_notification(diff)
            if texts:
                api = get_messaging_api()
                for text in texts[:5]:
                    api.push_message(
                        PushMessageRequest(
                            to=MY_LINE_USER_ID,
                            messages=[TextMessage(text=text)],
                        )
                    )
                logger.info(f"更新通知送信完了: {len(texts)}件のメッセージ")
    except Exception as e:
        logger.error(f"更新チェック失敗: {e}")

    # お気に入り薬のステータス変化チェック
    check_favorites_and_notify()


def check_favorites_and_notify():
    """登録済みお気に入り薬のステータスをチェックし、変化があれば通知"""
    all_favs = favorites.get_all_favorites()
    if not all_favs:
        return

    logger.info(f"お気に入りチェック: {len(all_favs)}件")
    api = get_messaging_api()

    for fav in all_favs:
        user_id = fav["user_id"]
        drug_name = fav["drug_name"]
        last_status = fav["last_status"]

        try:
            results = dsjp.search_drug(drug_name)
            if not results:
                current_status = "リストに記載なし"
            else:
                current_status = results[0].get("status", "不明")

            if last_status is None:
                favorites.update_last_status(user_id, drug_name, current_status)
                logger.info(f"初回ステータス記録: {drug_name} → {current_status}")
                continue

            if current_status != last_status:
                msg = (
                    f"⭐ お気に入り薬のステータスが変わりました\n"
                    f"━━━━━━━━━━━━━━━\n"
                    f"💊 {drug_name}\n"
                    f"　変更前：{last_status}\n"
                    f"　変更後：{current_status}\n"
                    f"━━━━━━━━━━━━━━━\n"
                    f"出典：厚生労働省"
                )
                api.push_message(PushMessageRequest(
                    to=user_id,
                    messages=[TextMessage(text=msg)],
                ))
                favorites.update_last_status(user_id, drug_name, current_status)
                logger.info(f"お気に入り変化通知: {drug_name} {last_status} → {current_status}")
        except Exception as e:
            logger.error(f"お気に入りチェックエラー ({drug_name}): {e}")


# ── スケジューラー設定 ─────────────────────────────
def start_scheduler():
    jst = pytz.timezone("Asia/Tokyo")
    scheduler = BackgroundScheduler(timezone=jst)
    scheduler.add_job(
        check_and_notify,
        trigger="cron",
        hour=14,
        minute=0,
        id="update_check",
    )
    scheduler.start()
    logger.info("スケジューラー起動: 毎日14時(JST)に更新チェック")
    return scheduler


# ── ヘルスチェック ────────────────────────────────
@app.route("/health", methods=["GET"])
def health():
    return {"status": "ok", "time": datetime.now().isoformat()}


# ── デバッグ：薬名検索の確認 ──────────────────────
@app.route("/debug-search", methods=["GET"])
def debug_search():
    """薬名検索の動作確認用エンドポイント"""
    keyword = request.args.get("keyword", "ノルバスク")
    results = dsjp.search_drug(keyword)
    return jsonify({
        "keyword": keyword,
        "count": len(results),
        "results": results[:5],
    })


@app.route("/debug-new", methods=["GET"])
def debug_new():
    """最新Newフラグ品目の確認用エンドポイント"""
    items = dsjp.get_new_items()
    return jsonify({
        "count": len(items),
        "items": items[:10],
    })


@app.route("/debug-columns", methods=["GET"])
def debug_columns():
    """Excelの列構造確認用エンドポイント（列名と先頭3行の中身を表示）"""
    df = dsjp._get_df()
    if df.empty:
        return jsonify({"error": "Excelの取得に失敗しました"})
    sample = df.head(3)
    columns_info = []
    for i, col in enumerate(df.columns):
        values = [str(v) for v in sample.iloc[:, i].tolist()]
        columns_info.append({
            "index": i,
            "column_name": str(col),
            "sample_values": values,
        })
    return jsonify({
        "total_rows": len(df),
        "total_cols": len(df.columns),
        "columns": columns_info,
    })


# ── Excelデータを起動時にプリロード ──────────────
def _preload_excel():
    """起動後すぐにExcelをバックグラウンドで取得してキャッシュする"""
    try:
        dsjp._get_df()
        logger.info("Excelデータのプリロード完了")
    except Exception as e:
        logger.error(f"Excelプリロード失敗: {e}")


# ── 起動 ──────────────────────────────────────────
if __name__ == "__main__":
    favorites.init_db()
    scheduler = start_scheduler()
    import threading
    threading.Thread(target=_preload_excel, daemon=True).start()
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
else:
    # Gunicorn経由で起動する場合もスケジューラーを開始
    favorites.init_db()
    scheduler = start_scheduler()
    import threading
    threading.Thread(target=_preload_excel, daemon=True).start()
