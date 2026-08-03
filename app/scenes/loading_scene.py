import tkinter as tk
from app.scenes.base_scene import SceneBase
import config

class LoadingScene(SceneBase):
    """判定中（ローディング）画面 (SC-04)"""
    
    def __init__(self, parent: tk.Widget, controller) -> None:
        super().__init__(parent, controller)
        self.configure(bg="#FFF8E7")

        # L-01: ローディング文言
        self.loading_label = tk.Label(
            self, 
            text="AIが考え中…", 
            font=("", 40, "bold"), 
            bg="#FFF8E7", 
            fg="#29B6F6"  # アクセントカラー
        )
        self.loading_label.pack(expand=True)

    def on_show(self, **kwargs) -> None:
        # --- テーマカラーの適用 ---
        colors = config.get_theme_colors()
        self.configure(bg=colors["bg"])
        self.loading_label.config(
            bg=colors["bg"], 
            fg=colors.get("accent", colors["primary"])
        )
        # ------------------------

        # この画面ではユーザーに何も操作させないため、キーボードの入力を無効化します
        self.focus_set()
        self.bind("<Any-KeyPress>", lambda e: "break")