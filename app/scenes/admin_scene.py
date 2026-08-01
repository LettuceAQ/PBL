import tkinter as tk
from app.scenes.base_scene import SceneBase

class AdminScene(SceneBase):
    """管理者用画面 (SC-99)"""
    
    def __init__(self, parent: tk.Widget, controller) -> None:
        super().__init__(parent, controller)
        self.configure(bg="#263238")  # 管理画面らしい少しダークな背景

        center_frame = tk.Frame(self, bg="#263238")
        center_frame.pack(expand=True)

        # タイトル
        tk.Label(
            center_frame,
            text="【管理者メニュー】",
            font=("", 28, "bold"),
            bg="#263238",
            fg="#ECEFF1"
        ).pack(pady=(0, 20))

        # プレイ件数などの簡易ステータス表示用ラベル
        self.status_label = tk.Label(
            center_frame,
            text="システム稼働中\nタイムアウト設定: 適用中",
            font=("", 18),
            bg="#263238",
            fg="#B0BEC5",
            justify="center"
        )
        self.status_label.pack(pady=10)

        # 操作ボタン用のフレーム
        btn_frame = tk.Frame(center_frame, bg="#263238")
        btn_frame.pack(pady=20)

        # 強制リセット（タイトルに戻る）ボタン
        self.reset_btn = tk.Button(
            btn_frame,
            text="タイトルに戻る [Esc]",
            font=("", 20, "bold"),
            bg="#EF5350",
            fg="white",
            width=20,
            command=self._on_back_to_title
        )
        self.reset_btn.pack(side="left", padx=10)

        # アプリ終了ボタン
        self.exit_btn = tk.Button(
            btn_frame,
            text="アプリを終了 [Q]",
            font=("", 20, "bold"),
            bg="#78909C",
            fg="white",
            width=16,
            command=self._on_exit_app
        )
        self.exit_btn.pack(side="left", padx=10)

    def on_show(self, **kwargs) -> None:
        self.focus_set()
        
        # ショートカットキーのバインド
        self.bind("<Escape>", lambda e: self._on_back_to_title())
        self.bind("q", lambda e: self._on_exit_app())

    def _on_back_to_title(self):
        # タイトル画面へ戻る
        self.controller.reset()

    def _on_exit_app(self):
        # アプリケーション全体を終了する
        self.controller.root.destroy()