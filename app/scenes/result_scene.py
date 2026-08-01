import tkinter as tk
from app.scenes.base_scene import SceneBase

class ResultScene(SceneBase):
    """結果／フィードバック画面 (SC-05)[cite: 1]"""
    
    def __init__(self, parent: tk.Widget, controller) -> None:
        super().__init__(parent, controller)
        self.configure(bg="#FFF8E7")

        # R-01: 選出画像表示領域（仮）[cite: 1]
        self.image_label = tk.Label(
            self, 
            text="[ここに選ばれた画像が出ます]", 
            font=("", 24), 
            bg="lightgray", 
            width=40, height=10
        )
        self.image_label.pack(pady=(40, 20))

        # R-03: フィードバック文表示領域[cite: 1]
        self.feedback_label = tk.Label(
            self, text="", font=("", 28, "bold"), bg="#FFF8E7", fg="#FFB74D"
        )
        self.feedback_label.pack(pady=20)

        # R-04: もう一度挑戦するボタン[cite: 1]
        self.retry_btn = tk.Button(
            self, text="もう一度挑戦する", font=("", 24, "bold"),
            bg="#29B6F6", fg="white", width=20,
            command=self._on_retry
        )
        self.retry_btn.pack(pady=20)

    def on_show(self, **kwargs) -> None:
        # コントローラーから受け取った情報を画面にセットする
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