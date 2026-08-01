import tkinter as tk
from app.scenes.base_scene import SceneBase
from PIL import Image, ImageTk
import os

class ResultScene(SceneBase):
    """結果／フィードバック画面 (SC-05)[cite: 1]"""
    
    def __init__(self, parent: tk.Widget, controller) -> None:
        super().__init__(parent, controller)
        self.configure(bg="#FFF8E7")

        # R-01: 選出画像表示領域
        self.image_label = tk.Label(self, bg="#FFF8E7")
        self.image_label.pack(pady=(10, 5))

        # R-03: フィードバック文表示領域
        self.feedback_label = tk.Label(
            self, text="", font=("", 20, "bold"), bg="#FFF8E7", fg="#FFB74D",
            wraplength=750, justify="center"
        )
        self.feedback_label.pack(pady=5)

        self.btn_frame = tk.Frame(self, bg="#FFF8E7")
        self.btn_frame.pack(pady=(5, 10))

        # R-04: もう一度挑戦するボタン (Enterキー対応)
        self.retry_btn = tk.Button(
            self.btn_frame, text="もう一度挑戦する [Enter]", font=("", 20, "bold"),
            bg="#29B6F6", fg="white", width=22, command=self._on_retry
        )
        self.retry_btn.pack(side="left", padx=10)
        
        # R-05: おわる（終了する）ボタン (Escキー対応)
        self.end_btn = tk.Button(
            self.btn_frame, text="おわる [Esc]", font=("", 20, "bold"),
            bg="#FF9800", fg="white", width=18, command=self._on_end
        )
        self.end_btn.pack(side="left", padx=10)
        
        self.current_photo = None

    def on_show(self, **kwargs) -> None:
        self.focus_set()
        
        best_img = kwargs.get("best_image", {})
        feedbacks = kwargs.get("feedbacks", [])
        self.is_finished = kwargs.get("is_finished", False)
        
        img_filename = best_img.get("file")
        if img_filename:
            img_path = os.path.join("data", "images", img_filename)
            if os.path.exists(img_path):
                pil_image = Image.open(img_path)
                pil_image = pil_image.resize((300, 300))
                self.current_photo = ImageTk.PhotoImage(pil_image)
                self.image_label.config(image=self.current_photo, text="")
            else:
                self.image_label.config(image='', text="[画像が見つかりません]", font=("", 20))
        
        feedback_text = "\n\n".join(feedbacks)
        self.feedback_label.config(text=feedback_text)
        
        if self.is_finished:
            # 3回目（上限到達）のときはリトライを消し、「おわる」をEnterキーで押せるようにする
            self.retry_btn.pack_forget()
            self.end_btn.config(text="次へ進む [Enter]")
            self.bind("<Return>", lambda e: self._on_end())
        else:
            # 1・2回目のときは両方表示し、Enterでリトライ、Escで「おわる」にする
            if not self.retry_btn.winfo_ismapped():
                self.retry_btn.pack(side="left", padx=10)
            self.end_btn.config(text="おわる [Esc]")
            
            # キーの割り当て
            self.bind("<Return>", lambda e: self._on_retry())
            self.bind("<Escape>", lambda e: self._on_end()) # ここを <space> から <Escape> に変更

    def _on_retry(self):
        self.controller.next_scene("input")
        
    def _on_end(self):
        self.controller.next_scene("end")