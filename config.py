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

# デフォルト設定値
IDLE_TIMEOUT_SEC = 30
MAX_ATTEMPTS = 3
MASTER_VOLUME = 80
SE_VOLUME = 100
THEME = "light"

# --- 新規追加する設定項目のデフォルト値 ---
ENABLE_TIMER = True          # 制限時間の有無 (True: 有効, False: 無効)
TIME_LIMIT_SEC = 60          # 制限時間（秒）
LOADING_DELAY_MS = 1500      # ローディング演出の待ち時間 (ミリ秒)
UI_SCALE = 1.0               # 画面全体のサイズ倍率 (1.0, 1.25, 1.5 など)
IS_FULLSCREEN = False        # フルスクリーン切替
DEBUG_MODE = False           # デバッグ情報の表示 (内部タグやFPSの可視化)

# 画面のデフォルト基準サイズ
BASE_WINDOW_WIDTH = 800
BASE_WINDOW_HEIGHT = 600

# カラーテーマ
COLOR_BG = "#FFF8E7"          # 背景色（明るいクリーム色）
COLOR_PRIMARY = "#FF9800"     # メインカラー（オレンジ）
COLOR_ACCENT = "#29B6F6"      # アクセントカラー（水色）
COLOR_FEEDBACK = "#FFB74D"    # フィードバック文字色


def load_config() -> None:
    """起動時にJSONファイルから設定を読み込む"""
    global IDLE_TIMEOUT_SEC, MAX_ATTEMPTS, MASTER_VOLUME, SE_VOLUME, THEME
    global ENABLE_TIMER, TIME_LIMIT_SEC, LOADING_DELAY_MS, UI_SCALE, IS_FULLSCREEN, DEBUG_MODE
    
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                IDLE_TIMEOUT_SEC = data.get("idle_timeout_sec", IDLE_TIMEOUT_SEC)
                MAX_ATTEMPTS = data.get("max_attempts", MAX_ATTEMPTS)
                MASTER_VOLUME = data.get("master_volume", MASTER_VOLUME)
                SE_VOLUME = data.get("se_volume", SE_VOLUME)
                THEME = data.get("theme", THEME)
                
                ENABLE_TIMER = data.get("enable_timer", ENABLE_TIMER)
                TIME_LIMIT_SEC = data.get("time_limit_sec", TIME_LIMIT_SEC)
                LOADING_DELAY_MS = data.get("loading_delay_ms", LOADING_DELAY_MS)
                UI_SCALE = data.get("ui_scale", UI_SCALE)
                IS_FULLSCREEN = data.get("is_fullscreen", IS_FULLSCREEN)
                DEBUG_MODE = data.get("debug_mode", DEBUG_MODE)
        except Exception as e:
            print(f"設定ファイルの読み込みに失敗しました: {e}")


def save_config(
    idle_sec: int, max_attempts: int, master_vol: int, se_vol: int, theme: str,
    enable_timer: bool, time_limit_sec: int, loading_delay_ms: int,
    ui_scale: float, is_fullscreen: bool, debug_mode: bool
) -> None:
    """設定をメモリ上に反映し、JSONファイルに保存する"""
    global IDLE_TIMEOUT_SEC, MAX_ATTEMPTS, MASTER_VOLUME, SE_VOLUME, THEME
    global ENABLE_TIMER, TIME_LIMIT_SEC, LOADING_DELAY_MS, UI_SCALE, IS_FULLSCREEN, DEBUG_MODE
    
    IDLE_TIMEOUT_SEC = idle_sec
    MAX_ATTEMPTS = max_attempts
    MASTER_VOLUME = master_vol
    SE_VOLUME = se_vol
    THEME = theme
    
    ENABLE_TIMER = enable_timer
    TIME_LIMIT_SEC = time_limit_sec
    LOADING_DELAY_MS = loading_delay_ms
    UI_SCALE = ui_scale
    IS_FULLSCREEN = is_fullscreen
    DEBUG_MODE = debug_mode
    
    data = {
        "idle_timeout_sec": IDLE_TIMEOUT_SEC,
        "max_attempts": MAX_ATTEMPTS,
        "master_volume": MASTER_VOLUME,
        "se_volume": SE_VOLUME,
        "theme": THEME,
        "enable_timer": ENABLE_TIMER,
        "time_limit_sec": TIME_LIMIT_SEC,
        "loading_delay_ms": LOADING_DELAY_MS,
        "ui_scale": UI_SCALE,
        "is_fullscreen": IS_FULLSCREEN,
        "debug_mode": DEBUG_MODE
    }
    try:
        os.makedirs(os.path.dirname(CONFIG_FILE), exist_ok=True)
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
    except Exception as e:
        print(f"設定ファイルの保存に失敗しました: {e}")


def get_theme_colors() -> dict:
    """現在のテーマに応じたカラーセットを返す"""
    if THEME == "dark":
        return {
            "bg": "#2C3E50",         # 背景（ダーク）
            "fg": "#ECF0F1",         # メイン文字色（白っぽい）
            "primary": "#E67E22",    # 強調カラー（オレンジ系）
            "secondary": "#BDC3C7",  # サブ文字・枠線など
            "card_bg": "#34495E"     # パーツやプレースホルダーの背景
        }
    else:
        return {
            "bg": "#FFF8E7",         # 背景（クリーム色）
            "fg": "#333333",         # メイン文字色（黒っぽい）
            "primary": "#FF9800",    # 強調カラー（オレンジ）
            "secondary": "#666666",  # サブ文字・枠線など
            "card_bg": "lightgray"   # パーツやプレースホルダーの背景
        }


# モジュール読み込み時に自動で設定をロードする
load_config()