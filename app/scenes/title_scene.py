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
            font=("", 28, "bold"), 
            bg="#FFF8E7", 
            fg="#FF9800"
        )
        self.title_label.pack(pady=(15, 5))

        # 待機イラストまたは長文テキストを表示するためのコンテナ（フレーム）
        self.content_frame = tk.Frame(self, bg="#FFF8E7")
        self.content_frame.pack(pady=5)

        # ① 画像表示用ラベル
        self.image_label = tk.Label(self.content_frame, bg="#FFF8E7")

        # ② テキスト表示用ボックス（テキストが長い場合でも全部入り切るようにスクロール対応のTextウィジェットを使用）
        self.text_widget = tk.Text(
            self.content_frame,
            font=("", 11),
            width=75,
            height=14,
            wrap="word",            # 単語の途中で折り返さないようにする
            bd=2,
            relief="solid"
        )
        # スクロールバーも添える場合
        self.scrollbar = tk.Scrollbar(self.content_frame, command=self.text_widget.yview)
        self.text_widget.config(yscrollcommand=self.scrollbar.set)

        # T-02: 操作案内文言
        self.guide_label = tk.Label(
            self, 
            text="なにかキーを押してね", 
            font=("", 18, "bold"), 
            bg="#FFF8E7"
        )
        self.guide_label.pack(pady=(10, 15))
        
        self.current_photo = None

    def on_show(self, **kwargs) -> None:
        """画面が表示されたときにテーマカラーの適用とイラストの読み込みを行う"""
        self.focus_set()

        # --- テーマカラーの適用 ---
        colors = config.get_theme_colors()
        self.configure(bg=colors["bg"])
        self.content_frame.config(bg=colors["bg"])
        self.title_label.config(bg=colors["bg"], fg=colors["primary"])
        self.guide_label.config(bg=colors["bg"], fg=colors["fg"])
        # ------------------------

        # 1. 待機イラスト画像（title_illust.png）の読み込み試行
        img_path = os.path.join("data", "images", "title_illust.png")
        
        if os.path.exists(img_path):
            try:
                pil_image = Image.open(img_path)
                pil_image = pil_image.resize((280, 180)) # 画像サイズ
                self.current_photo = ImageTk.PhotoImage(pil_image)
                
                # 画像を表示し、テキストボックスは隠す
                self.text_widget.pack_forget()
                self.scrollbar.pack_forget()
                self.image_label.config(image=self.current_photo, text="", bg=colors["bg"])
                self.image_label.pack()
                return
            except Exception:
                pass

        # 2. 画像がない場合はテキストファイルの内容をTextウィジェットに流し込む
        self.image_label.pack_forget()
        
        text_path = os.path.join("data", "title_placeholder_text.txt")
        display_text = "[待機イラスト表示領域]"
        
        if os.path.exists(text_path):
            try:
                with open(text_path, "r", encoding="utf-8") as f:
                    display_text = f.read().strip()
            except Exception:
                pass

        # Textウィジェットに文字をセット
        self.text_widget.config(
            state="normal",
            bg="white" if config.THEME == "light" else "#34495E",
            fg="#333333" if config.THEME == "light" else "#ECF0F1",
            insertbackground="#333333" if config.THEME == "light" else "#ECF0F1"
        )
        self.text_widget.delete("1.0", tk.END)
        self.text_widget.insert("1.0", display_text)
        self.text_widget.config(state="disabled") # 編集不可（閲覧専用）にする

        # テキストボックスとスクロールバーを表示
        self.text_widget.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        # キーバインドの登録
        for char in "abcdefghijklmnopqrstuvwxyz":
            self.bind(f"<Key-{char}>", self._on_valid_key_press)
            self.bind(f"<Key-{char.upper()}>", self._on_valid_key_press)
        
        for num in "0123456789":
            self.bind(f"<Key-{num}>", self._on_valid_key_press)
        
        self.bind("<Return>", self._on_valid_key_press)
        self.bind("<space>", self._on_valid_key_press)
        self.bind("<F12>", lambda e: self.controller.next_scene("admin"))

    def _on_valid_key_press(self, event):
        self.controller.start_new_session()