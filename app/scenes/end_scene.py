import tkinter as tk
from app.scenes.base_scene import SceneBase
import config

class EndScene(SceneBase):
    """終了メッセージ画面 (SC-06)"""
    
    def __init__(self, parent: tk.Widget, controller) -> None:
        super().__init__(parent, controller)
        self.configure(bg="#FFF8E7")

        # E-01: メインメッセージ
        self.title_label = tk.Label(
            self, 
            text="SEはコンピュータに伝える仕事です", 
            font=("", 36, "bold"), 
            bg="#FFF8E7",
            fg="#FF9800"
        )
        self.title_label.pack(pady=(80, 40))

        # E-02: 体験のまとめ文
        summary_text = (
            "言葉が足りないと、AIにはうまく伝わりません。\n\n"
            "AIやコンピュータに、どうすれば正確に伝わるか？\n"
            "それを考えるのが、システムエンジニア（SE）のお仕事です！\n\n"
            "体験してくれてありがとう！"
        )
        self.summary_label = tk.Label(
            self, 
            text=summary_text, 
            font=("", 24), 
            bg="#FFF8E7",
            justify="center"
        )
        self.summary_label.pack(pady=20)

        # 案内文
        self.guide_label = tk.Label(
            self, 
            text="最初に戻る（Enterキー）", 
            font=("", 24), 
            bg="#FFF8E7",
            fg="#29B6F6"
        )
        self.guide_label.pack(pady=40)

    def on_show(self, **kwargs) -> None:
        # --- テーマカラーの適用 ---
        colors = config.get_theme_colors()
        self.configure(bg=colors["bg"])
        self.title_label.config(bg=colors["bg"], fg=colors["primary"])
        self.summary_label.config(bg=colors["bg"], fg=colors["fg"])
        self.guide_label.config(
            bg=colors["bg"], 
            fg=colors.get("accent", colors["primary"])
        )
        # ------------------------

        self.focus_set()
        # Enterキーでタイトル画面に戻り、次の人のためのリセットを行う
        self.bind("<Return>", self._on_enter_press)

    def _on_enter_press(self, event):
        self.controller.reset() # コントローラーにリセットを指示