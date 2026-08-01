import tkinter as tk
from app.scenes.base_scene import SceneBase
import config
from app.core.play_logger import PlayLogger

class AdminScene(SceneBase):
    """管理者用画面 (SC-99)"""
    
    def __init__(self, parent: tk.Widget, controller) -> None:
        super().__init__(parent, controller)
        self.configure(bg="#263238")  # 管理画面らしいダークな背景
        self.logger = PlayLogger()    # ロガーの準備

        center_frame = tk.Frame(self, bg="#263238")
        center_frame.pack(expand=True)

        # タイトル
        tk.Label(
            center_frame,
            text="【管理者メニュー（設定変更）】",
            font=("", 26, "bold"),
            bg="#263238",
            fg="#ECEFF1"
        ).pack(pady=(0, 20))

        # --- 設定変更用の入力フレーム ---
        form_frame = tk.Frame(center_frame, bg="#263238")
        form_frame.pack(pady=10)

        # 1. タイムアウト秒数の設定
        tk.Label(
            form_frame, text="無操作タイムアウト (秒):", font=("", 18), bg="#263238", fg="#CFD8DC"
        ).grid(row=0, column=0, sticky="w", pady=8, padx=10)
        
        self.idle_var = tk.StringVar()
        self.idle_entry = tk.Entry(form_frame, textvariable=self.idle_var, font=("", 18), width=8)
        self.idle_entry.grid(row=0, column=1, pady=8, padx=10)

        # 2. 最大試行回数の設定
        tk.Label(
            form_frame, text="最大試行回数 (回):", font=("", 18), bg="#263238", fg="#CFD8DC"
        ).grid(row=1, column=0, sticky="w", pady=8, padx=10)
        
        self.attempts_var = tk.StringVar()
        self.attempts_entry = tk.Entry(form_frame, textvariable=self.attempts_var, font=("", 18), width=8)
        self.attempts_entry.grid(row=1, column=1, pady=8, padx=10)

        # 適用ボタン
        self.apply_btn = tk.Button(
            center_frame,
            text="設定を保存して適用する",
            font=("", 18, "bold"),
            bg="#4CAF50",
            fg="white",
            width=22,
            command=self._on_apply_config
        )
        self.apply_btn.pack(pady=15)

        # メッセージ表示用
        self.msg_label = tk.Label(
            center_frame, text="", font=("", 16), bg="#263238", fg="#81C784"
        )
        self.msg_label.pack(pady=5)

        # --- 操作ボタン用のフレーム ---
        btn_frame = tk.Frame(center_frame, bg="#263238")
        btn_frame.pack(pady=15)

        # 強制リセット（タイトルに戻る）ボタン
        self.reset_btn = tk.Button(
            btn_frame,
            text="タイトルに戻る [Esc]",
            font=("", 18, "bold"),
            bg="#EF5350",
            fg="white",
            width=18,
            command=self._on_back_to_title
        )
        self.reset_btn.pack(side="left", padx=10)

        # アプリ終了ボタン
        self.exit_btn = tk.Button(
            btn_frame,
            text="アプリを終了 [Q]",
            font=("", 18, "bold"),
            bg="#78909C",
            fg="white",
            width=16,
            command=self._on_exit_app
        )
        self.exit_btn.pack(side="left", padx=10)

    def on_show(self, **kwargs) -> None:
        self.focus_set()
        self.idle_var.set(str(config.IDLE_TIMEOUT_SEC))
        self.attempts_var.set(str(config.MAX_ATTEMPTS))
        self.msg_label.config(text="")
        
        self.bind("<Escape>", lambda e: self._on_back_to_title())
        self.bind("q", lambda e: self._on_exit_app())

    def _on_apply_config(self):
        try:
            new_idle = int(self.idle_var.get())
            new_attempts = int(self.attempts_var.get())
            
            if new_idle <= 0 or new_attempts <= 0:
                raise ValueError()

            # 設定をファイルに保存して永続化
            config.save_config(new_idle, new_attempts)
            
            # ーーー 追加：管理者設定の変更履歴をCSVに記録する ーーー
            self.logger.log_admin_change(new_idle, new_attempts)
            
            self.msg_label.config(text="✔ 設定を保存し、ログに記録しました！", fg="#81C784")
        except ValueError:
            self.msg_label.config(text="⚠ 正しい数値を入力してください", fg="#E57373")

    def _on_back_to_title(self):
        self.controller.reset()

    def _on_exit_app(self):
        self.controller.root.destroy()