import tkinter as tk
from app.scenes.base_scene import SceneBase

class LoadingScene(SceneBase):
    """判定中（ローディング）画面 (SC-04)[cite: 1]"""
    
    def __init__(self, parent: tk.Widget, controller) -> None:
        super().__init__(parent, controller)
        self.configure(bg="#FFF8E7")

        # L-01: ローディング文言[cite: 1]
        self.loading_label = tk.Label(
            self, 
            text="AIが考え中…", 
            font=("", 40, "bold"), 
            bg="#FFF8E7", 
            fg="#29B6F6"  # アクセントカラー
        )
        self.loading_label.pack(expand=True)

    def on_show(self, **kwargs) -> None:
        # この画面ではユーザーに何も操作させないため、キーボードの入力を無効化します
        self.focus_set()
        self.bind("<Any-KeyPress>", lambda e: "break")