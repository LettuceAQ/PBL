import tkinter as tk
from app.scenes.base_scene import SceneBase
from PIL import Image, ImageTk
import os

class ResultScene(SceneBase):
    """結果／フィードバック画面 (SC-05)"""
    
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

        # ーーー 常に左側に「もう一度挑戦する（または次のステップ）」ボタンを配置 ーーー
        self.left_btn = tk.Button(
            self.btn_frame, text="もう一度挑戦する [Enter]", font=("", 20, "bold"),
            bg="#29B6F6", fg="white", width=22, command=self._on_left_click
        )
        self.left_btn.pack(side="left", padx=10)
        
        # ーーー 常に右側に「おわる」ボタンを配置 ーーー
        self.right_btn = tk.Button(
            self.btn_frame, text="おわる [Esc]", font=("", 20, "bold"),
            bg="#FF9800", fg="white", width=18, command=self._on_right_click
        )
        self.right_btn.pack(side="left", padx=10)
        
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
        
        # ーーー 状態に応じてボタンの文字と機能を切り替える（位置は絶対に変わらない） ーーー
        if self.is_finished:
            # 3回目（上限到達）のとき：左側を「次へ進む」に変え、Enterですすめる
            self.left_btn.config(
                text="次へ進む [Enter]", 
                bg="#4CAF50", 
                width=18
            )
            # 右側はそのまま「おわる [Esc]」
            self.right_btn.config(
                text="おわる [Esc]",
                bg="#FF9800"
            )
            
            self.bind("<Return>", lambda e: self._on_right_click()) # 3回目はEnterでおわる（終了画面へ）
            self.bind("<Escape>", lambda e: self._on_right_click())
        else:
            # 1・2回目のとき：左側を「もう一度挑戦する」、右側を「おわる」にする
            self.left_btn.config(
                text="もう一度挑戦する [Enter]", 
                bg="#29B6F6", 
                width=22
            )
            self.right_btn.config(
                text="おわる [Esc]", 
                bg="#FF9800",
                width=18
            )
            
            self.bind("<Return>", lambda e: self._on_retry())
            self.bind("<Escape>", lambda e: self._on_end())

    def _on_left_click(self):
        if self.is_finished:
            self._on_end()
        else:
            self._on_retry()

    def _on_right_click(self):
        self._on_end()

    def _on_retry(self):
        self.controller.next_scene("input")
        
    def _on_end(self):
        self.controller.next_scene("end")