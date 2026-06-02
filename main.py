import shutil
import os
import logging
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

# --- バージョン管理 ---
VERSION = "v1.0"

# --- ⚙️ ログの設定 ---
LOG_FILE = Path(__file__).parent / "desktop_cleaner.log"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[
        logging.FileHandler(LOG_FILE, encoding="utf-8", mode="a"),
        logging.StreamHandler()
    ]
)

# .env からパスを取得
DESKTOP_DIR = Path(os.environ.get("DESKTOP_DIR"))
TARGET_DIR = Path(os.environ.get("TARGET_DIR"))
EXCLUDE_EXTS = set(os.environ.get("EXCLUDE_EXTS", "").split(","))

def main():
    logging.info("デスクトップのお掃除を開始します:" + VERSION)
    # 🔥 設定されたパスを最初にログに残す（環境の確認用）
    logging.info(f"[設定] 監視元: {DESKTOP_DIR}")
    logging.info(f"[設定] 移動先: {TARGET_DIR}")
    
    # フォルダの存在チェック
    if not DESKTOP_DIR.exists():
        logging.error(f"デスクトップフォルダが見つかりません: {DESKTOP_DIR}")
        return

    if not TARGET_DIR.exists():
        try:
            TARGET_DIR.mkdir(parents=True, exist_ok=True)
            logging.info(f"移動先フォルダを作成しました: {TARGET_DIR}")
        except Exception as e:
            logging.error(f"移動先フォルダの作成に失敗しました: {e}", exc_info=True)
            return

    moved_count = 0

    # デスクトップ内のアイテムを順番に確認
    for item in DESKTOP_DIR.iterdir():
        
        if item.is_file() and item.suffix.lower() not in EXCLUDE_EXTS:
            target_path = TARGET_DIR / item.name
            
            try:
                # ファイルを移動する
                shutil.move(str(item), str(target_path))
                # 🔥 移動先のフルパス（target_path）をログに出力するように変更
                logging.info(f"[移動済] {item.name} -> {target_path}")
                moved_count += 1
                
            except Exception as e:
                # 🔥 失敗時も「どこへ」移動しようとしてダメだったか分かるように変更
                logging.error(f"[失敗] {item.name} を {target_path} へ移動できませんでした。エラー: {e}", exc_info=True)

    logging.info(f"--- お掃除が完了しました（移動数: {moved_count}件） ---")

if __name__ == "__main__":
    main()