import tkinter as tk
from app.scenes.base_scene import SceneBase
from PIL import Image, ImageTk
import os

class TopicScene(SceneBase):
    """お題提示画面 (SC-02)"""
    
    def __init__(self, parent: tk.Widget, controller) -> None:
        super().__init__(parent, controller)
        self.configure(bg="#FFF8E7")

        # 画面全体を綺麗に配置するためのフレーム
        center_frame = tk.Frame(self, bg="#FFF8E7")
        center_frame.pack(expand=True)

        # ーーー 修正：答えになってしまう具体的なタイトル文字列の代わりに、共通の案内文を表示 ーーー
        self.instruction_label = tk.Label(
            center_frame,
            text="この画像のとおりに、AIに伝えてね！",
            font=("", 28, "bold"),
            bg="#FFF8E7",
            fg="#FF9800"
        )
        self.instruction_label.pack(pady=(0, 20))

        # 参照画像を表示するラベル
        self.image_label = tk.Label(center_frame, bg="#FFF8E7")
        self.image_label.pack(pady=10)

        # 操作案内
        self.guide_label = tk.Label(
            center_frame,
            text="はじめる [Enter]",
            font=("", 24, "bold"),
            bg="#FFF8E7",
            fg="#29B6F6"
        )
        self.guide_label.pack(pady=(20, 0))

        self.current_photo = None

    def on_show(self, **kwargs) -> None:
        self.focus_set()
        
        # コントローラーから渡されたお題データを受け取る
        topic = kwargs.get("topic", {})
        ref_img_id = topic.get("reference_image")

        # 参照画像ファイルを探して表示する
        img_filename = f"{ref_img_id}.png"
        img_path = os.path.join("data", "images", img_filename)
        
        if os.path.exists(img_path):
            pil_image = Image.open(img_path)
            pil_image = pil_image.resize((300, 300))
            self.current_photo = ImageTk.PhotoImage(pil_image)
            self.image_label.config(image=self.current_photo, text="")
        else:
            self.image_label.config(image="", text="[参照画像がありません]", font=("", 20))

        # Enterキー(Return)が押されたら入力画面へ遷移する
        self.bind("<Return>", self._on_enter_press)

    def _on_enter_press(self, event):
        self.controller.next_scene("input")