import tkinter as tk

class GameController:
    """画面遷移とゲーム全体の進行を統括するクラス"""
    
    def __init__(self, root: tk.Tk) -> None:
        self.root = root

    def start(self) -> None:
        """アプリを起動し、初期画面を表示する（仮実装）"""
        # 画面の真ん中にテスト用の文字を表示します
        label = tk.Label(
            self.root, 
            text="システム起動成功！\nAIに伝われ！〜SEのおしごと体験〜", 
            font=("", 32)
        )
        label.pack(expand=True)