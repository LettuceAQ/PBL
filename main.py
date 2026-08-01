import tkinter as tk
import atexit
import sys
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
    
    # 終了フラグ（正常終了かどうかを判定するため）
    is_normal_shutdown = False

    def handle_normal_exit():
        nonlocal is_normal_shutdown
        if not is_normal_shutdown:
            is_normal_shutdown = True
            logger.log_system("SHUTDOWN", "アプリケーションが正常に終了しました")

    # atexitを使って通常のスクリプト終了時にフックする
    atexit.register(handle_normal_exit)

    controller = GameController(root)
    controller.start()

    # ウィンドウの×ボタンが押されたときのイベントハンドラ
    def on_closing():
        nonlocal is_normal_shutdown
        is_normal_shutdown = True
        logger.log_system("SHUTDOWN", "ウィンドウの×ボタンにより正常終了しました")
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_closing)

    try:
        root.mainloop()
    except Exception as e:
        # メインループ内でキャッチされなかった致命的エラー（強制終了扱い）
        logger.log_system("CRASH", f"未処理の例外により異常終了しました: {e}")
        raise e

if __name__ == "__main__":
    main()