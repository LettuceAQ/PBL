import tkinter as tk
from app.scenes.base_scene import SceneBase

class ResultScene(SceneBase):
    """結果／フィードバック画面 (SC-05)[cite: 1]"""
    
    def __init__(self, parent: tk.Widget, controller) -> None:
        super().__init__(parent, controller)
        self.configure(bg="#FFF8E7")

        # R-01: 選出画像表示領域（仮）[cite: 1]
        # 高さを10から8に減らし、上下の余白(pady)も詰めます
        self.image_label = tk.Label(
            self, 
            text="[ここに選ばれた画像が出ます]", 
            font=("", 24), 
            bg="lightgray", 
            width=40, height=8 
        )
        self.image_label.pack(pady=(20, 10))

        # R-03: フィードバック文表示領域[cite: 1]
        # 文字サイズを 28 から 24 に小さくし、余白も減らします
        self.feedback_label = tk.Label(
            self, 
            text="", 
            font=("", 24, "bold"), 
            bg="#FFF8E7", 
            fg="#FFB74D",
            wraplength=750,  # 幅も少し広げて改行数を減らします
            justify="center"
        )
        self.feedback_label.pack(pady=10)

        # R-04: もう一度挑戦するボタン[cite: 1]
        self.retry_btn = tk.Button(
            self, text="もう一度挑戦する", font=("", 24, "bold"),
            bg="#29B6F6", fg="white", width=20,
            command=self._on_retry
        )
        self.retry_btn.pack(pady=(10, 20))

    def on_show(self, **kwargs) -> None:
        best_img = kwargs.get("best_image", {})
        feedbacks = kwargs.get("feedbacks", [])
        
        img_id = best_img.get("id", "不明な画像")
        self.image_label.config(text=f"[ AIが選んだ画像: {img_id} ]")
        
        # フィードバックのリストを改行でつないで表示
        feedback_text = "\n\n".join(feedbacks)
        self.feedback_label.config(text=feedback_text)

    def _on_retry(self):
        # 入力画面に戻る
        self.controller.next_scene("input")