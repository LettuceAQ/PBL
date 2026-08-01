import tkinter as tk
from app.scenes.base_scene import SceneBase

class TopicScene(SceneBase):
    """お題提示画面 (SC-02)"""
    
    def __init__(self, parent: tk.Widget, controller) -> None:
        super().__init__(parent, controller)
        self.configure(bg="#FFF8E7") # 背景色[cite: 2]

        # Q-01: お題文（仮置き）
        self.topic_label = tk.Label(
            self,
            text="【お題】\n\n赤い帽子をかぶった犬",
            font=("", 40, "bold"),
            bg="#FFF8E7"
        )
        self.topic_label.pack(expand=True)

        # Q-02: 操作案内[cite: 1]
        self.guide_label = tk.Label(
            self,
            text="はじめる（Enterキー）",
            font=("", 24),
            bg="#FFF8E7",
            fg="#29B6F6"  # アクセントカラーの水色[cite: 2]
        )
        self.guide_label.pack(pady=50)

    def on_show(self, **kwargs) -> None:
        self.focus_set()
        # Enterキー(Return)が押されたら入力画面へ遷移する
        self.bind("<Return>", self._on_enter_press)

    def _on_enter_press(self, event):
        # 次の画面（入力画面）へ遷移[cite: 1]
        self.controller.next_scene("input")