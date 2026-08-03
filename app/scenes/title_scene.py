import tkinter as tk
from app.scenes.base_scene import SceneBase

class TitleScene(SceneBase):
    """タイトル画面 (SC-01)"""
    
    def __init__(self, parent: tk.Widget, controller) -> None:
        super().__init__(parent, controller)
        
        # 背景色の設定（明るいクリーム色）
        self.configure(bg="#FFF8E7")

        # --- 画面レイアウト設計 (基本設計書 3.2, 12) ---
        
        # T-01: タイトル文言
        self.title_label = tk.Label(
            self, 
            text="AIに伝われ！\n〜SEのおしごと体験〜", 
            font=("", 40, "bold"), 
            bg="#FFF8E7", 
            fg="#FF9800"  # メインカラーのオレンジ
        )
        self.title_label.pack(pady=(80, 40))

        # 待機イラスト表示領域（仮の灰色の枠）
        self.image_placeholder = tk.Label(
            self,
            text="[待機イラスト表示領域]",
            font=("", 20),
            bg="lightgray",
            width=40,
            height=10
        )
        self.image_placeholder.pack(pady=20)

        # T-02: 操作案内文言
        self.guide_label = tk.Label(
            self, 
            text="なにかキーを押してね", 
            font=("", 28), 
            bg="#FFF8E7"
        )
        self.guide_label.pack(pady=(40, 50))
        
    def on_show(self, **kwargs) -> None:
        """画面が表示されたときにキー入力を受け付ける準備をする"""
        self.focus_set()

        # 1. アルファベット（a〜z、大文字・小文字）を許可
        for char in "abcdefghijklmnopqrstuvwxyz":
            self.bind(f"<Key-{char}>", self._on_valid_key_press)
            self.bind(f"<Key-{char.upper()}>", self._on_valid_key_press)
        
        # 2. 数字（0〜9）を許可
        for num in "0123456789":
            self.bind(f"<Key-{num}>", self._on_valid_key_press)
        
        # 3. Enterキーとスペースキーを許可
        self.bind("<Return>", self._on_valid_key_press)
        self.bind("<space>", self._on_valid_key_press)
        self.bind("<backspace>", self._on_valid_key_press)

        # 4. スタッフ用隠しコマンド（F12キーで管理者画面へ）
        self.bind("<F12>", lambda e: self.controller.next_scene("admin"))

    def _on_valid_key_press(self, event):
        """許可されたキーが押されたときの処理"""
        self.controller.start_new_session()