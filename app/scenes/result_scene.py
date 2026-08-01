import tkinter as tk
from app.scenes.base_scene import SceneBase

class ResultScene(SceneBase):
    """結果／フィードバック画面 (SC-05)[cite: 1]"""
    
    def __init__(self, parent: tk.Widget, controller) -> None:
        super().__init__(parent, controller)
        self.configure(bg="#FFF8E7")

        self.image_label = tk.Label(
            self, 
            text="[ここに選ばれた画像が出ます]", 
            font=("", 24), 
            bg="lightgray", 
            width=40, height=8 
        )
        self.image_label.pack(pady=(20, 10))

        self.feedback_label = tk.Label(
            self, 
            text="", 
            font=("", 24, "bold"), 
            bg="#FFF8E7", 
            fg="#FFB74D",
            wraplength=750,
            justify="center"
        )
        self.feedback_label.pack(pady=10)

        self.btn_frame = tk.Frame(self, bg="#FFF8E7")
        self.btn_frame.pack(pady=(10, 20))

        # R-04: もう一度挑戦するボタン[cite: 1]
        self.retry_btn = tk.Button(
            self.btn_frame, text="もう一度挑戦する (Enter)", font=("", 24, "bold"),
            bg="#29B6F6", fg="white", width=25,
            command=self._on_retry
        )
        self.retry_btn.pack(side="left", padx=10)
        
        # R-05: おわる（終了する）ボタン[cite: 1]
        self.end_btn = tk.Button(
            self.btn_frame, text="次へ進む (Enter)", font=("", 24, "bold"),
            bg="#FF9800", fg="white", width=25,
            command=self._on_end
        )

    def on_show(self, **kwargs) -> None:
        # 画面が表示されたらフォーカスを自身に当てる（キー入力を受け取るため）
        self.focus_set()
        
        best_img = kwargs.get("best_image", {})
        feedbacks = kwargs.get("feedbacks", [])
        self.is_finished = kwargs.get("is_finished", False)  # クラス変数として保持する
        
        img_id = best_img.get("id", "不明な画像")
        self.image_label.config(text=f"[ AIが選んだ画像: {img_id} ]")
        
        feedback_text = "\n\n".join(feedbacks)
        self.feedback_label.config(text=feedback_text)
        
        if self.is_finished:
            # 3回終わっていた場合
            self.retry_btn.pack_forget()
            self.end_btn.pack(side="left", padx=10)
            # Enterキーを「次へ」に紐付ける
            self.bind("<Return>", lambda e: self._on_end())
        else:
            # まだ挑戦できる場合
            self.end_btn.pack_forget()
            self.retry_btn.pack(side="left", padx=10)
            # Enterキーを「リトライ」に紐付ける
            self.bind("<Return>", lambda e: self._on_retry())

    def _on_retry(self):
        self.controller.next_scene("input")
        
    def _on_end(self):
        self.controller.next_scene("end")