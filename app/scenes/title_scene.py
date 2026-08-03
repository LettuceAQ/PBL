import tkinter as tk
from app.scenes.base_scene import SceneBase
from PIL import Image, ImageTk
import config
import os

class TitleScene(SceneBase):
    """タイトル画面 (SC-01)"""
    
    def __init__(self, parent: tk.Widget, controller) -> None:
        super().__init__(parent, controller)
        
        # 背景色の設定
        self.configure(bg="#FFF8E7")

        # T-01: タイトル文言
        self.title_label = tk.Label(
            self, 
            text="AIに伝われ！\n〜SEのおしごと体験〜", 
            font=("", 40, "bold"), 
            bg="#FFF8E7", 
            fg="#FF9800"
        )
        self.title_label.pack(pady=(50, 20))

        # 待機イラスト表示領域（画像またはテキストを表示）
        self.image_placeholder = tk.Label(
            self,
            font=("", 20),
            bg="lightgray",
            width=40,
            height=10
        )
        self.image_placeholder.pack(pady=10)

        # T-02: 操作案内文言
        self.guide_label = tk.Label(
            self, 
            text="なにかキーを押してね", 
            font=("", 28), 
            bg="#FFF8E7"
        )
        self.guide_label.pack(pady=(20, 30))
        
        self.current_photo = None

    def on_show(self, **kwargs) -> None:
        """画面が表示されたときにテーマカラーの適用とイラストの読み込みを行う"""
        self.focus_set()

        # --- テーマカラーの適用 ---
        colors = config.get_theme_colors()
        self.configure(bg=colors["bg"])
        self.title_label.config(bg=colors["bg"], fg=colors["primary"])
        self.guide_label.config(bg=colors["bg"], fg=colors["fg"])
        # ------------------------

        # 1. 待機イラスト画像（title_illust.png）の読み込み試行
        img_path = os.path.join("data", "images", "title_illust.png")
        
        if os.path.exists(img_path):
            try:
                pil_image = Image.open(img_path)
                pil_image = pil_image.resize((300, 200)) # 必要に応じてサイズ調整
                self.current_photo = ImageTk.PhotoImage(pil_image)
                self.image_placeholder.config(image=self.current_photo, text="", bg=colors["bg"])
            except Exception:
                self._load_fallback_text(colors)
        else:
            # 2. 画像がない場合はテキストファイルから読み込む
            self._load_fallback_text(colors)

        # キーバインドの登録
        for char in "abcdefghijklmnopqrstuvwxyz":
            self.bind(f"<Key-{char}>", self._on_valid_key_press)
            self.bind(f"<Key-{char.upper()}>", self._on_valid_key_press)
        
        for num in "0123456789":
            self.bind(f"<Key-{num}>", self._on_valid_key_press)
        
        self.bind("<Return>", self._on_valid_key_press)
        self.bind("<space>", self._on_valid_key_press)
        self.bind("<F12>", lambda e: self.controller.next_scene("admin"))

    def _load_fallback_text(self, colors) -> None:
        """画像が見つからない場合にテキストファイルから文言を読み込んで表示する"""
        text_path = os.path.join("data", "title_placeholder_text.txt")
        display_text = "[待機イラスト表示領域]"
        
        if os.path.exists(text_path):
            try:
                with open(text_path, "r", encoding="utf-8") as f:
                    display_text = f.read().strip()
            except Exception:
                pass

        self.image_placeholder.config(
            image="",
            text=display_text,
            bg=colors["card_bg"],
            fg=colors["fg"]
        )

    def _on_valid_key_press(self, event):
        self.controller.start_new_session()