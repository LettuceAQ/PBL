import csv
import os
from datetime import datetime

class PlayLogger:
    """プレイログおよび管理者設定変更ログを記録するクラス"""
    
    def __init__(self, log_dir: str = "logs") -> None:
        self.log_dir = log_dir
        self.play_log_path = os.path.join(log_dir, "play_log.csv")
        self.admin_log_path = os.path.join(log_dir, "admin_log.csv")
        self._initialize_files()

    def _initialize_files(self) -> None:
        """ログファイルが存在しない場合、ヘッダー行を作成して初期化する"""
        os.makedirs(self.log_dir, exist_ok=True)
        
        # 1. プレイログの初期化
        if not os.path.exists(self.play_log_path):
            with open(self.play_log_path, "w", encoding="utf-8-sig", newline="") as f:
                writer = csv.writer(f)
                writer.writerow([
                    "timestamp",       # 記録日時
                    "topic_id",        # お題ID
                    "attempt_count",   # 何回目の試行か
                    "input_prompt",    # 入力されたプロンプト
                    "extracted_tags",  # 抽出されたタグ
                    "matched_image",   # 選出された画像ID
                    "feedbacks"        # 表示されたフィードバック
                ])

        # 2. 管理者設定変更ログの初期化
        if not os.path.exists(self.admin_log_path):
            with open(self.admin_log_path, "w", encoding="utf-8-sig", newline="") as f:
                writer = csv.writer(f)
                writer.writerow([
                    "timestamp",       # 変更日時
                    "idle_timeout_sec",# 変更後のタイムアウト秒数
                    "max_attempts"     # 変更後の最大試行回数
                ])

    def log_attempt(self, topic_id: str, attempt_count: int, prompt: str, tags: list, matched_image: str, feedbacks: list) -> None:
        """1回の試行データをCSVに追記する"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        tags_str = ", ".join(tags) if isinstance(tags, list) else str(tags)
        feedbacks_str = " / ".join(feedbacks) if isinstance(feedbacks, list) else str(feedbacks)

        try:
            with open(self.play_log_path, "a", encoding="utf-8-sig", newline="") as f:
                writer = csv.writer(f)
                writer.writerow([
                    timestamp,
                    topic_id,
                    attempt_count,
                    prompt,
                    tags_str,
                    matched_image,
                    feedbacks_str
                ])
        except Exception as e:
            print(f"プレイログの書き込みに失敗しました: {e}")

    def log_admin_change(self, idle_sec: int, max_attempts: int) -> None:
        """管理者による設定変更データをCSVに追記する"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        try:
            with open(self.admin_log_path, "a", encoding="utf-8-sig", newline="") as f:
                writer = csv.writer(f)
                writer.writerow([
                    timestamp,
                    idle_sec,
                    max_attempts
                ])
        except Exception as e:
            print(f"管理者ログの書き込みに失敗しました: {e}")