import csv
import os
from datetime import datetime

class PlayLogger:
    """プレイログ、管理者変更ログ、エラーログ、システムログを記録するクラス"""
    
    def __init__(self, log_dir: str = "logs") -> None:
        self.log_dir = log_dir
        self.play_log_path = os.path.join(log_dir, "play_log.csv")
        self.admin_log_path = os.path.join(log_dir, "admin_log.csv")
        self.error_log_path = os.path.join(log_dir, "error_log.csv")
        self.system_log_path = os.path.join(log_dir, "system_log.csv")
        self._initialize_files()

    def _initialize_files(self) -> None:
        """ログファイルが存在しない場合、ヘッダー行を作成して初期化する"""
        os.makedirs(self.log_dir, exist_ok=True)
        
        # 1. プレイログの初期化
        if not os.path.exists(self.play_log_path):
            with open(self.play_log_path, "w", encoding="utf-8-sig", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(["timestamp", "topic_id", "attempt_count", "input_prompt", "extracted_tags", "matched_image", "feedbacks"])

        # 2. 管理者設定変更ログの初期化
        if not os.path.exists(self.admin_log_path):
            with open(self.admin_log_path, "w", encoding="utf-8-sig", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(["timestamp", "idle_timeout_sec", "max_attempts"])

        # 3. エラーログの初期化
        if not os.path.exists(self.error_log_path):
            with open(self.error_log_path, "w", encoding="utf-8-sig", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(["timestamp", "location", "error_message"])

        # 4. システムライフサイクルログの初期化
        if not os.path.exists(self.system_log_path):
            with open(self.system_log_path, "w", encoding="utf-8-sig", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(["timestamp", "event_type", "details"])

    def log_attempt(self, topic_id: str, attempt_count: int, prompt: str, tags: list, matched_image: str, feedbacks: list) -> None:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        tags_str = ", ".join(tags) if isinstance(tags, list) else str(tags)
        feedbacks_str = " / ".join(feedbacks) if isinstance(feedbacks, list) else str(feedbacks)
        try:
            with open(self.play_log_path, "a", encoding="utf-8-sig", newline="") as f:
                writer = csv.writer(f)
                writer.writerow([timestamp, topic_id, attempt_count, prompt, tags_str, matched_image, feedbacks_str])
        except Exception as e:
            print(f"プレイログの書き込みに失敗しました: {e}")

    def log_admin_change(self, idle_sec: int, max_attempts: int) -> None:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        try:
            with open(self.admin_log_path, "a", encoding="utf-8-sig", newline="") as f:
                writer = csv.writer(f)
                writer.writerow([timestamp, idle_sec, max_attempts])
        except Exception as e:
            print(f"管理者ログの書き込みに失敗しました: {e}")

    def log_error(self, location: str, error_message: str) -> None:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        try:
            with open(self.error_log_path, "a", encoding="utf-8-sig", newline="") as f:
                writer = csv.writer(f)
                writer.writerow([timestamp, location, error_message])
        except Exception as e:
            print(f"エラーログの書き込みに失敗しました: {e}")

    def log_system(self, event_type: str, details: str = "") -> None:
        """アプリの起動・終了などのライフサイクルイベントを記録する"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        try:
            with open(self.system_log_path, "a", encoding="utf-8-sig", newline="") as f:
                writer = csv.writer(f)
                writer.writerow([timestamp, event_type, details])
        except Exception as e:
            print(f"システムログの書き込みに失敗しました: {e}")