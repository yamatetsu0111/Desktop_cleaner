import shutil
import os
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

# .env からパスを取得（設定されていなければカレントディレクトリをデフォルトにする工夫も◎）
DESKTOP_DIR = Path(os.environ.get("DESKTOP_DIR"))
TARGET_DIR = Path(os.environ.get("TARGET_DIR"))

# 拡張子も文字から集合(set)に変換する
EXCLUDE_EXTS = set(os.environ.get("EXCLUDE_EXTS").split(","))

def main():
    # 移動先フォルダが存在しない場合は自動作成する
    if not TARGET_DIR.exists():
        TARGET_DIR.mkdir(parents=True, exist_ok=True)

    print("--- デスクトップのお掃除を開始します ---")

    # デスクトップ内のアイテムを順番に確認
    for item in DESKTOP_DIR.iterdir():
        
        # 条件1: フォルダではなく「ファイル」であること
        # 条件2: 拡張子（小文字）が除外リストに含まれていないこと
        if item.is_file() and item.suffix.lower() not in EXCLUDE_EXTS:
            
            target_path = TARGET_DIR / item.name
            
            try:
                # ファイルを移動する
                shutil.move(str(item), str(target_path))
                print(f"[移動済] {item.name}")
            except Exception as e:
                # 移動先に同じ名前のファイルが既にある場合などのエラー回避
                print(f"[スキップ] {item.name} （エラー: {e}）")

    print("\n--- お掃除が完了しました ---")

if __name__ == "__main__":
    main()