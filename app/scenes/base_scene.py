import tkinter as tk

class SceneBase(tk.Frame):
    """全Sceneクラスの基底クラス[cite: 1]"""
    
    def __init__(self, parent: tk.Widget, controller) -> None:
        super().__init__(parent)
        self.controller = controller

    def on_show(self, **kwargs) -> None:
        """画面表示時に呼び出される。前画面からのデータを受け取る[cite: 1]"""
        pass

    def on_hide(self) -> None:
        """画面が非表示になる際に呼び出される（後始末処理）[cite: 1]"""
        pass