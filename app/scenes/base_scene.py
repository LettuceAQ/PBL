import tkinter as tk
import config  # config.pyを読み込む

class SceneBase(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

    def on_show(self, **kwargs):
        """どの画面が表示されるときも、共通でこのメソッドが呼ばれます"""
        # 1. config.py の設定（theme）を確認して色を決める
        if getattr(config, "THEME", "light") == "dark":
            bg_color = "#2C3E50"  # ダークテーマの背景色（落ち着いた紺色）
        else:
            bg_color = "#FFF8E7"  # ライトテーマの背景色（明るいクリーム色）

        # 2. 画面全体の背景色を自動で適用する
        self.configure(bg=bg_color)

    def on_hide(self) -> None:
        """画面が非表示になる際に呼び出される（後始末処理）[cite: 1]"""
        pass