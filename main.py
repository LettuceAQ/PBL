import tkinter as tk
from app.controller import GameController

def main():
    # ウィンドウの作成
    root = tk.Tk()
    root.title("AIに伝われ！〜SEのおしごと体験〜")
    
    # 画面サイズの設定（いったん800x600のウィンドウモードで起動します）
    root.geometry("800x600")
    
    # GameControllerを呼び出して開始
    app = GameController(root)
    app.start()
    
    # アプリの画面を表示し続ける
    root.mainloop()

if __name__ == "__main__":
    main()