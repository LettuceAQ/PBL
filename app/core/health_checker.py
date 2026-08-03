import os
import sys

class HealthChecker:
    """起動時に必要なファイルやフォルダの存在を自己診断するクラス"""
    
    @staticmethod
    def check_environment() -> tuple[bool, str]:
        """
        環境をチェックする。
        Returns:
            (is_ok: bool, error_message: str)
        """
        if getattr(sys, 'frozen', False):
            base_dir = os.path.dirname(sys.executable)
        else:
            base_dir = os.getcwd()

        # 必須フォルダのチェック
        data_dir = os.path.join(base_dir, "data")
        logs_dir = os.path.join(base_dir, "logs")
        images_dir = os.path.join(data_dir, "images")

        if not os.path.exists(data_dir):
            return False, f"必須フォルダが見つかりません:\n{data_dir}\n(dataフォルダを配置してください)"

        if not os.path.exists(images_dir):
            return False, f"画像フォルダが見つかりません:\n{images_dir}\n(imagesフォルダを配置してください)"

        # 必須JSONファイルのチェック
        required_files = [
            "topics.json",
            "tags.json",
            "synonyms.json",
            "keyword_tag_map.json",
            "feedback_messages.json",
            "config.json"
        ]

        missing_files = []
        for filename in required_files:
            file_path = os.path.join(data_dir, filename)
            if not os.path.exists(file_path):
                missing_files.append(filename)

        if missing_files:
            return False, f"以下の必須設定ファイルが不足しています:\n{', '.join(missing_files)}\n\n(dataフォルダ内を確認してください)"

        # logsフォルダがない場合は自動作成を試みる
        if not os.path.exists(logs_dir):
            try:
                os.makedirs(logs_dir, exist_ok=True)
            except Exception as e:
                return False, f"ログフォルダ(logs)の作成に失敗しました: {e}"

        return True, "OK"