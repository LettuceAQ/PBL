import tkinter as tk
from app.scenes.base_scene import SceneBase
# ーーー 追加：画像処理ライブラリ Pillow の読み込み ーーー
from PIL import Image, ImageTk
import os

class ResultScene(SceneBase):
    """結果／フィードバック画面 (SC-05)[cite: 1]"""
    
    def __init__(self, parent: tk.Widget, controller) -> None:
        super().__init__(parent, controller)
        self.configure(bg="#FFF8E7")

        # R-01: 選出画像表示領域[cite: 1]
        self.image_label = tk.Label(self, bg="#FFF8E7")
        self.image_label.pack(pady=(20, 10))

        # R-03: フィードバック文表示領域[cite: 1]
        self.feedback_label = tk.Label(
            self, text="", font=("", 24, "bold"), bg="#FFF8E7", fg="#FFB74D",
            wraplength=750, justify="center"
        )
        self.feedback_label.pack(pady=10)

        self.btn_frame = tk.Frame(self, bg="#FFF8E7")
        self.btn_frame.pack(pady=(10, 20))

        # R-04: もう一度挑戦するボタン
        self.retry_btn = tk.Button(
            self.btn_frame, text="もう一度挑戦する (Enter)", font=("", 24, "bold"),
            bg="#29B6F6", fg="white", width=25, command=self._on_retry
        )
        # R-05: おわる（終了する）ボタン
        self.end_btn = tk.Button(
            self.btn_frame, text="次へ進む (Enter)", font=("", 24, "bold"),
            bg="#FF9800", fg="white", width=25, command=self._on_end
        )
        
        # 画面に表示する画像を保持しておく変数（これがないと画像が消えてしまう）
        self.current_photo = None

    def on_show(self, **kwargs) -> None:
        self.focus_set()
        
        best_img = kwargs.get("best_image", {})
        feedbacks = kwargs.get("feedbacks", [])
        self.is_finished = kwargs.get("is_finished", False)
        
        # ーーー 修正：実際の画像を読み込んで表示する ーーー
        img_filename = best_img.get("file")
        if img_filename:
            img_path = os.path.join("data", "images", img_filename)
            if os.path.exists(img_path):
                # Pillowで画像を開き、Tkinter用に変換する
                pil_image = Image.open(img_path)
                # サイズ調整が必要な場合はここでリサイズ (FR-07)[cite: 2]
                pil_image = pil_image.resize((400, 400))
                self.current_photo = ImageTk.PhotoImage(pil_image)
                # Labelに画像をセット
                self.image_label.config(image=self.current_photo, text="")
            else:
                self.image_label.config(image='', text="[画像が見つかりません]", font=("", 24))
        
        feedback_text = "\n\n".join(feedbacks)
        self.feedback_label.config(text=feedback_text)
        
        if self.is_finished:
            self.retry_btn.pack_forget()
            self.end_btn.pack(side="left", padx=10)
            self.bind("<Return>", lambda e: self._on_end())
        else:
            self.end_btn.pack_forget()
            self.retry_btn.pack(side="left", padx=10)
            self.bind("<Return>", lambda e: self._on_retry())

    def _on_retry(self):
        self.controller.next_scene("input")
        
    def _on_end(self):
        self.controller.next_scene("end")