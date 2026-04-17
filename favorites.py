"""
favorites.py - お気に入り薬の登録・管理モジュール

Supabase PostgreSQL に接続して favorites テーブルを操作する。
DATABASE_URL 環境変数に接続文字列を設定すること。
"""

import os
import logging
import psycopg2
from psycopg2.extras import RealDictCursor

logger = logging.getLogger(__name__)

DATABASE_URL = os.environ.get("DATABASE_URL", "")


def _get_conn():
    """DB接続を取得する"""
    return psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)


def init_db():
    """favoritesテーブルが存在しない場合は作成する"""
    if not DATABASE_URL:
        logger.warning("DATABASE_URLが設定されていません。お気に入り機能は無効です。")
        return
    try:
        with _get_conn() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS favorites (
                        id SERIAL PRIMARY KEY,
                        user_id TEXT NOT NULL,
                        drug_name TEXT NOT NULL,
                        last_status TEXT,
                        created_at TIMESTAMP DEFAULT NOW(),
                        UNIQUE(user_id, drug_name)
                    )
                """)
            conn.commit()
        logger.info("favoritesテーブル初期化完了")
    except Exception as e:
        logger.error(f"DB初期化エラー: {e}")


def add_favorite(user_id: str, drug_name: str) -> str:
    """お気に入りに薬を追加する。戻り値はユーザーへのメッセージ。"""
    if not DATABASE_URL:
        return "お気に入り機能は現在利用できません。"
    try:
        with _get_conn() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO favorites (user_id, drug_name)
                    VALUES (%s, %s)
                    ON CONFLICT (user_id, drug_name) DO NOTHING
                    """,
                    (user_id, drug_name),
                )
                if cur.rowcount == 0:
                    return f"「{drug_name}」はすでに登録済みです。"
            conn.commit()
        return f"✅ 「{drug_name}」をお気に入りに登録しました。\nステータスが変化したらお知らせします。"
    except Exception as e:
        logger.error(f"お気に入り登録エラー: {e}")
        return "登録中にエラーが発生しました。"


def remove_favorite(user_id: str, drug_name: str) -> str:
    """お気に入りから薬を削除する。戻り値はユーザーへのメッセージ。"""
    if not DATABASE_URL:
        return "お気に入り機能は現在利用できません。"
    try:
        with _get_conn() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "DELETE FROM favorites WHERE user_id = %s AND drug_name = %s",
                    (user_id, drug_name),
                )
                if cur.rowcount == 0:
                    return f"「{drug_name}」はお気に入りに登録されていません。"
            conn.commit()
        return f"🗑 「{drug_name}」をお気に入りから削除しました。"
    except Exception as e:
        logger.error(f"お気に入り削除エラー: {e}")
        return "削除中にエラーが発生しました。"


def list_favorites(user_id: str) -> list:
    """ユーザーのお気に入り一覧を返す。[{"drug_name": ..., "last_status": ...}, ...]"""
    if not DATABASE_URL:
        return []
    try:
        with _get_conn() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT drug_name, last_status FROM favorites WHERE user_id = %s ORDER BY created_at",
                    (user_id,),
                )
                return [dict(row) for row in cur.fetchall()]
    except Exception as e:
        logger.error(f"お気に入り一覧取得エラー: {e}")
        return []


def get_all_favorites() -> list:
    """全ユーザーのお気に入りを返す（通知チェック用）。[{"user_id": ..., "drug_name": ..., "last_status": ...}, ...]"""
    if not DATABASE_URL:
        return []
    try:
        with _get_conn() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT user_id, drug_name, last_status FROM favorites ORDER BY user_id")
                return [dict(row) for row in cur.fetchall()]
    except Exception as e:
        logger.error(f"全お気に入り取得エラー: {e}")
        return []


def update_last_status(user_id: str, drug_name: str, status: str):
    """お気に入りのlast_statusを更新する"""
    if not DATABASE_URL:
        return
    try:
        with _get_conn() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "UPDATE favorites SET last_status = %s WHERE user_id = %s AND drug_name = %s",
                    (status, user_id, drug_name),
                )
            conn.commit()
    except Exception as e:
        logger.error(f"last_status更新エラー: {e}")
