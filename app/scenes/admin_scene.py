import tkinter as tk
from tkinter import ttk
from app.scenes.base_scene import SceneBase
from app.core.play_logger import PlayLogger
import config
import sys
import os

class AdminScene(SceneBase):
    """管理者設定画面 (SC-06) - タブ化されたゲーム風オプション"""
    
    def __init__(self, parent: tk.Widget, controller) -> None:
        super().__init__(parent, controller)
        self.configure(bg="#2C3E50") # 少し落ち着いたゲーム風のダークトーン背景

        self.logger = PlayLogger()

        # タイトルヘッダー
        header_label = tk.Label(
            self, text="⚙ OPTIONS / 管理者設定", 
            font=("", 24, "bold"), bg="#2C3E50", fg="#ECF0F1"
        )
        header_label.pack(pady=(20, 10))

        # ーーー ノートブック（タブ）の作成 ーーー
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TNotebook', background='#2C3E50', borderwidth=0)
        style.configure('TNotebook.Tab', font=('', 14, 'bold'), padding=[15, 8])

        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True, padx=30, pady=10)

        # 各タブ用のフレーム
        self.tab_game = tk.Frame(self.notebook, bg="#34495E")
        self.tab_audio = tk.Frame(self.notebook, bg="#34495E")
        self.tab_theme = tk.Frame(self.notebook, bg="#34495E")

        self.notebook.add(self.tab_game, text=" 🎮 ゲーム設定 ")
        self.notebook.add(self.tab_audio, text=" 🔊 オーディオ ")
        self.notebook.add(self.tab_theme, text=" 🎨 外観・テーマ ")

        # 各タブの中身をビルド
        self._build_game_tab()
        self._build_audio_tab()
        self._build_theme_tab()

        # ーーー アプリ内メッセージ表示ラベル ーーー
        self.status_label = tk.Label(
            self, text="", font=("", 12, "bold"), bg="#2C3E50", fg="#2ECC71"
        )
        self.status_label.pack(pady=(0, 5))

        # ーーー 画面下部の共通操作ボタンエリア ーーー
        btn_frame = tk.Frame(self, bg="#2C3E50")
        btn_frame.pack(fill="x", padx=30, pady=(0, 20))

        save_btn = tk.Button(
            btn_frame, text="設定を保存 [Enter]", font=("", 16, "bold"),
            bg="#27AE60", fg="white", width=16, command=self._save_settings
        )
        save_btn.pack(side="left", padx=5)

        back_btn = tk.Button(
            btn_frame, text="タイトルへ戻る [Esc]", font=("", 16, "bold"),
            bg="#7F8C8D", fg="white", width=16, command=self._back_to_title
        )
        back_btn.pack(side="left", padx=5)

        exit_app_btn = tk.Button(
            btn_frame, text="アプリ終了 [Q]", font=("", 16, "bold"),
            bg="#C0392B", fg="white", width=14, command=self._exit_app
        )
        exit_app_btn.pack(side="right", padx=5)

        # キーバインド
        self.bind("<Escape>", lambda e: self._back_to_title())
        self.bind("<Return>", lambda e: self._save_settings())
        self.bind("q", lambda e: self._exit_app())
        self.bind("Q", lambda e: self._exit_app())

    def _build_game_tab(self) -> None:
        """ゲームプレイに関する設定タブ"""
        frame = self.tab_game
        
        tk.Label(frame, text="放置タイムアウト秒数 (秒):", font=("", 14), bg="#34495E", fg="white").pack(anchor="w", padx=30, pady=(30, 5))
        self.idle_entry = tk.Entry(frame, font=("", 14), width=10)
        self.idle_entry.pack(anchor="w", padx=30)
        tk.Label(frame, text="※無操作がこの秒数続くと自動でタイトル画面に戻ります。", font=("", 10), bg="#34495E", fg="#BDC3C7").pack(anchor="w", padx=30, pady=(2, 15))

        tk.Label(frame, text="最大試行回数 (回):", font=("", 14), bg="#34495E", fg="white").pack(anchor="w", padx=30, pady=(10, 5))
        self.max_attempt_entry = tk.Entry(frame, font=("", 14), width=10)
        self.max_attempt_entry.pack(anchor="w", padx=30)

    def _build_audio_tab(self) -> None:
        """音声・効果音に関する設定タブ"""
        frame = self.tab_audio
        
        tk.Label(frame, text="マスター音量:", font=("", 14), bg="#34495E", fg="white").pack(anchor="w", padx=30, pady=(30, 5))
        self.master_vol_slider = tk.Scale(frame, from_=0, to=100, orient="horizontal", bg="#34495E", fg="white", highlightbackground="#34495E", length=300)
        self.master_vol_slider.pack(anchor="w", padx=30)

        tk.Label(frame, text="SE (効果音) 音量:", font=("", 14), bg="#34495E", fg="white").pack(anchor="w", padx=30, pady=(20, 5))
        self.se_vol_slider = tk.Scale(frame, from_=0, to=100, orient="horizontal", bg="#34495E", fg="white", highlightbackground="#34495E", length=300)
        self.se_vol_slider.pack(anchor="w", padx=30)

    def _build_theme_tab(self) -> None:
        """外観・カラーに関する設定タブ"""
        frame = self.tab_theme
        
        tk.Label(frame, text="UI カラーテーマ:", font=("", 14), bg="#34495E", fg="white").pack(anchor="w", padx=30, pady=(30, 5))
        
        self.theme_var = tk.StringVar(value="light")
        tk.Radiobutton(frame, text="ライトテーマ (温かみのある標準)", variable=self.theme_var, value="light", font=("", 12), bg="#34495E", fg="white", selectcolor="#2C3E50").pack(anchor="w", padx=50, pady=5)
        tk.Radiobutton(frame, text="ダークテーマ (目に優しい暗色)", variable=self.theme_var, value="dark", font=("", 12), bg="#34495E", fg="white", selectcolor="#2C3E50").pack(anchor="w", padx=50, pady=5)

    def on_show(self, **kwargs) -> None:
        self.focus_set()
        # 画面を開くたびにステータスをクリア
        self.status_label.config(text="")

        # 現在の設定値を各入力コンポーネントに反映
        self.idle_entry.delete(0, tk.END)
        self.idle_entry.insert(0, str(config.IDLE_TIMEOUT_SEC))

        self.max_attempt_entry.delete(0, tk.END)
        self.max_attempt_entry.insert(0, str(config.MAX_ATTEMPTS))

        self.master_vol_slider.set(config.MASTER_VOLUME)
        self.se_vol_slider.set(config.SE_VOLUME)
        self.theme_var.set(config.THEME)

    def _save_settings(self) -> None:
        try:
            new_idle = int(self.idle_entry.get())
            new_max = int(self.max_attempt_entry.get())
            
            if new_idle <= 0 or new_max <= 0:
                raise ValueError("数値は1以上を指定してください。")

            new_master = self.master_vol_slider.get()
            new_se = self.se_vol_slider.get()
            new_theme = self.theme_var.get()

            # config.py の save_config 関数を使って一括保存・更新
            config.save_config(new_idle, new_max, new_master, new_se, new_theme)

            # ログに残す
            self.logger.log_admin_change(new_idle, new_max)

            # ポップアップを出さず、アプリ内に成功メッセージを表示する
            self.status_label.config(
                text="✔ 設定を正常に保存しました！", 
                fg="#2ECC71"
            )

        except ValueError as e:
            self.status_label.config(
                text=f"✖ 入力エラー: 正しい数値を入力してください ({e})", 
                fg="#E74C3C"
            )

    def _back_to_title(self) -> None:
        self.controller.next_scene("title")

    def _exit_app(self) -> None:
        from tkinter import messagebox
        if messagebox.askyesno("確認", "アプリケーションを終了しますか？"):
            self.logger.log_system("SHUTDOWN", "管理者画面から終了されました")
            self.controller.root.destroy()