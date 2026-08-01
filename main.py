import tkinter as tk
import atexit
import sys
import traceback
from app.controller import GameController
from app.core.play_logger import PlayLogger

def main():
    root = tk.Tk()
    root.title("AIに伝われ！〜SEのおしごと体験〜")
    root.geometry("800x600")
    
    # ロガーの準備
    logger = PlayLogger()
    
    # 1. 起動ログの記録
    logger.log_system("START", "アプリケーションが起動しました")
    
    is_normal_shutdown = False

    def handle_normal_exit():
        nonlocal is_normal_shutdown
        if not is_normal_shutdown:
            is_normal_shutdown = True
            logger.log_system("SHUTDOWN", "アプリケーションが正常に終了しました")

    atexit.register(handle_normal_exit)

    # ーーー 予期せぬクラッシュ（未処理の例外）をグローバルにフックする仕組み ーーー
    def global_exception_handler(exc_type, exc_value, exc_traceback):
        nonlocal is_normal_shutdown
        is_normal_shutdown = True
        
        # エラー詳細文字列を作成
        error_msg = "".join(traceback.format_exception(exc_type, exc_value, exc_traceback))
        
        # ログファイルに書き込む
        logger.log_error("Global.Crash", str(exc_value) + "\n" + error_msg)
        logger.log_system("CRASH", f"予期せぬ例外により異常終了しました: {exc_value}")
        
        # 通常のターミナル出力も維持する
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