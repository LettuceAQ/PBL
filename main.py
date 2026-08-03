import tkinter as tk
from tkinter import messagebox
import atexit
import sys
import traceback

from app.controller import GameController
from app.core.play_logger import PlayLogger
from app.core.health_checker import HealthChecker  # 追加

def main():
    # 1. 起動前の環境自己診断（ヘルスチェック）
    is_ok, error_msg = HealthChecker.check_environment()
    if not is_ok:
        # Tkのルートがまだないので一時的なウィンドウを作ってエラーを出す
        temp_root = tk.Tk()
        temp_root.withdraw()
        messagebox.showerror("起動エラー (環境チェック失敗)", error_msg)
        temp_root.destroy()
        sys.exit(1)

    root = tk.Tk()
    root.title("AIに伝われ！〜SEのおしごと体験〜")
    root.geometry("800x600")
    
    # ロガーの準備
    logger = PlayLogger()
    
    # 2. 起動ログの記録
    logger.log_system("START", "アプリケーションが起動しました")
    
    is_normal_shutdown = False

    def handle_normal_exit():
        nonlocal is_normal_shutdown
        if not is_normal_shutdown:
            is_normal_shutdown = True
            logger.log_system("SHUTDOWN", "アプリケーションが正常に終了しました")

    atexit.register(handle_normal_exit)

    def global_exception_handler(exc_type, exc_value, exc_traceback):
        nonlocal is_normal_shutdown
        is_normal_shutdown = True
        
        error_msg = "".join(traceback.format_exception(exc_type, exc_value, exc_traceback))
        logger.log_error("Global.Crash", str(exc_value) + "\n" + error_msg)
        logger.log_system("CRASH", f"予期せぬ例外により異常終了しました: {exc_value}")
        
        sys.__excepthook__(exc_type, exc_value, exc_traceback)

    sys.excepthook = global_exception_handler

    controller = GameController(root)
    controller.start()

    def on_closing():
        nonlocal is_normal_shutdown
        is_normal_shutdown = True
        logger.log_system("SHUTDOWN", "ウィンドウの×ボタンにより正常終了しました")
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_closing)

    root.mainloop()

if __name__ == "__main__":
    main()