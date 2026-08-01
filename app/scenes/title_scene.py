import tkinter as tk
from app.scenes.base_scene import SceneBase

class TitleScene(SceneBase):
    """タイトル画面 (SC-01)[cite: 1]"""
    
    def __init__(self, parent: tk.Widget, controller) -> None:
        super().__init__(parent, controller)
        
        # 背景色の設定（明るいクリーム色）[cite: 2]
        self.configure(bg="#FFF8E7")

        # --- 画面レイアウト設計 (基本設計書 3.2, 12) ---
        
        # T-01: タイトル文言[cite: 1]
        self.title_label = tk.Label(
            self, 
            text="AIに伝われ！\n〜SEのおしごと体験〜", 
            font=("", 40, "bold"), 
            bg="#FFF8E7", 
            fg="#FF9800"  # メインカラーのオレンジ[cite: 2]
        )
        self.title_label.pack(pady=(80, 40))

        # 待機イラスト表示領域（今回は仮の灰色の枠を置きます）[cite: 1]
        self.image_placeholder = tk.Label(
            self,
            text="[待機イラスト表示領域]",
            font=("", 20),
            bg="lightgray",
            width=40,
            height=10
        )
        self.image_placeholder.pack(pady=20)

        # T-02: 操作案内文言[cite: 1]
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
        # どのキーが押されても _on_key_press メソッドが呼ばれるようにする
        self.bind("<Any-KeyPress>", self._on_key_press)

        # ーーー 追加：スタッフ用隠しコマンド（F12キーで管理者画面へ） ーーー
        self.bind("<F12>", lambda e: self.controller.next_scene("admin"))

    def _on_key_press(self, event):
        """キーボードが押されたときの処理"""
        # 変更：新しいセッションを開始してお題画面へ
        self.controller.start_new_session()