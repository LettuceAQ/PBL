"""
システム全体の設定値を一元管理するファイル (ConfigManager)
展示会場の状況に合わせて、このファイルの数値を変更することで調整できます。
"""

# 無操作タイムアウトの秒数（テスト中は10秒、本番展示では30秒などに変更可能）
IDLE_TIMEOUT_SEC = 20

# 1セッションあたりの最大試行回数
MAX_ATTEMPTS = 2

# 判定中のローディング演出の時間（ミリ秒）
LOADING_DELAY_MS = 1300

# 画面のデフォルトサイズ
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

# カラーテーマ（基本設計書 17.1 に準拠）
COLOR_BG = "#FFF8E7"          # 背景色（明るいクリーム色）[cite: 2]
COLOR_PRIMARY = "#FF9800"     # メインカラー（オレンジ）[cite: 2]
COLOR_ACCENT = "#29B6F6"      # アクセントカラー（水色）[cite: 2]
COLOR_FEEDBACK = "#FFB74D"    # フィードバック文字色[cite: 2]