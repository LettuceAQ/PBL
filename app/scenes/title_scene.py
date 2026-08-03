import tkinter as tk
from app.scenes.base_scene import SceneBase
import config  # 追加

class TitleScene(SceneBase):
    """タイトル画面 (SC-01)"""
    
    def __init__(self, parent: tk.Widget, controller) -> None:
        super().__init__(parent, controller)
        
        # --- 画面レイアウト設計 ---
        # ウィジェット作成時は仮の色でOK（あとで on_show でテーマカラーが適用されます）
        self.title_label = tk.Label(
            self, 
            text="AIに伝われ！\n〜SEのおしごと体験〜", 
            font=("", 40, "bold")
        )
        self.title_label.pack(pady=(80, 40))

        self.image_placeholder = tk.Label(
            self,
            text="[待機イラスト表示領域]",
            font=("", 20),
            width=40,
            height=10
        )
        self.image_placeholder.pack(pady=20)

        self.guide_label = tk.Label(
            self, 
            text="なにかキーを押してね", 
            font=("", 28)
        )
        self.guide_label.pack(pady=(40, 50))
        
    def on_show(self, **kwargs) -> None:
        """画面が表示されたときにテーマカラーを適用し、キー入力を受け付ける"""
        self.focus_set()

        # 1. config から現在のテーマカラーをごっそり取得
        colors = config.get_theme_colors()

        # 2. 画面全体と各ウィジェットの色をテーマに合わせて一括変更！
        self.configure(bg=colors["bg"])
        self.title_label.config(bg=colors["bg"], fg=colors["primary"])
        self.image_placeholder.config(bg=colors["card_bg"], fg=colors["fg"])
        self.guide_label.config(bg=colors["bg"], fg=colors["fg"])

        # 3. キーバインドの登録
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