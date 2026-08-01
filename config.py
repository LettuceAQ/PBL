"""
システム全体の設定値を一元管理するファイル (ConfigManager)
JSONファイルと連携し、変更内容を永続化します。
"""
import json
import os
import sys

if getattr(sys, 'frozen', False):
    base_dir = os.path.dirname(sys.executable)
else:
    base_dir = os.getcwd()

CONFIG_FILE = os.path.join(base_dir, "data", "config.json")

# デフォルト値
IDLE_TIMEOUT_SEC = 30
MAX_ATTEMPTS = 3

# 画面のデフォルトサイズや演出時間（これらはコード側で固定管理）
LOADING_DELAY_MS = 1500
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

# カラーテーマ
COLOR_BG = "#FFF8E7"          # 背景色（明るいクリーム色）
COLOR_PRIMARY = "#FF9800"     # メインカラー（オレンジ）
COLOR_ACCENT = "#29B6F6"      # アクセントカラー（水色）
COLOR_FEEDBACK = "#FFB74D"    # フィードバック文字色


def load_config() -> None:
    """起動時にJSONファイルから設定を読み込む"""
    global IDLE_TIMEOUT_SEC, MAX_ATTEMPTS
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                IDLE_TIMEOUT_SEC = data.get("idle_timeout_sec", IDLE_TIMEOUT_SEC)
                MAX_ATTEMPTS = data.get("max_attempts", MAX_ATTEMPTS)
        except Exception as e:
            print(f"設定ファイルの読み込みに失敗しました: {e}")


def save_config(idle_sec: int, max_attempts: int) -> None:
    """設定をメモリ上に反映し、JSONファイルに保存する"""
    global IDLE_TIMEOUT_SEC, MAX_ATTEMPTS
    IDLE_TIMEOUT_SEC = idle_sec
    MAX_ATTEMPTS = max_attempts
    
    data = {
        "idle_timeout_sec": IDLE_TIMEOUT_SEC,
        "max_attempts": MAX_ATTEMPTS
    }
    try:
        os.makedirs(os.path.dirname(CONFIG_FILE), exist_ok=True)
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
    except Exception as e:
        print(f"設定ファイルの保存に失敗しました: {e}")


# モジュール読み込み時に自動で設定をロードする
load_config()            