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
        style.configure('TNotebook.Tab', font=('', 14, 'bold'), padding=[12, 8])

        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True, padx=30, pady=10)

        # 各タブ用のフレーム (ゲーム設定, オーディオ, 外観, システム・デバッグ)
        self.tab_game = tk.Frame(self.notebook, bg="#34495E")
        self.tab_audio = tk.Frame(self.notebook, bg="#34495E")
        self.tab_theme = tk.Frame(self.notebook, bg="#34495E")
        self.tab_system = tk.Frame(self.notebook, bg="#34495E")

        self.notebook.add(self.tab_game, text=" 🎮 ゲーム設定 ")
        self.notebook.add(self.tab_audio, text=" 🔊 オーディオ ")
        self.notebook.add(self.tab_theme, text=" 🎨 外観・表示 ")
        self.notebook.add(self.tab_system, text=" 🛠 システム・デバッグ ")

        # 各タブの中身をビルド
        self._build_game_tab()
        self._build_audio_tab()
        self._build_theme_tab()
        self._build_system_tab()

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
        
        # 放置タイムアウト
        tk.Label(frame, text="放置タイムアウト秒数 (秒):", font=("", 13), bg="#34495E", fg="white").pack(anchor="w", padx=30, pady=(15, 2))
        self.idle_entry = tk.Entry(frame, font=("", 13), width=10)
        self.idle_entry.pack(anchor="w", padx=30)

        # 最大試行回数
        tk.Label(frame, text="最大試行回数 (回):", font=("", 13), bg="#34495E", fg="white").pack(anchor="w", padx=30, pady=(10, 2))
        self.max_attempt_entry = tk.Entry(frame, font=("", 13), width=10)
        self.max_attempt_entry.pack(anchor="w", padx=30)

        # 制限時間（タイマー）の有無
        self.enable_timer_var = tk.BooleanVar(value=True)
        timer_check = tk.Checkbutton(
            frame, text="制限時間（タイマー）を有効にする", variable=self.enable_timer_var,
            font=("", 13), bg="#34495E", fg="white", selectcolor="#2C3E50", activebackground="#34495E", activeforeground="white"
        )
        timer_check.pack(anchor="w", padx=30, pady=(10, 2))

        # 制限時間（秒）
        tk.Label(frame, text="制限時間秒数 (秒):", font=("", 13), bg="#34495E", fg="white").pack(anchor="w", padx=30, pady=(5, 2))
        self.time_limit_entry = tk.Entry(frame, font=("", 13), width=10)
        self.time_limit_entry.pack(anchor="w", padx=30)

        # ローディング演出の待ち時間（秒）
        tk.Label(frame, text="ローディング演出時間 (秒):", font=("", 13), bg="#34495E", fg="white").pack(anchor="w", padx=30, pady=(10, 2))
        self.loading_delay_entry = tk.Entry(frame, font=("", 13), width=10)
        self.loading_delay_entry.pack(anchor="w", padx=30)
        tk.Label(frame, text="※「AIが考えています…」画面の表示時間（例: 1.5 秒）", font=("", 9), bg="#34495E", fg="#BDC3C7").pack(anchor="w", padx=30, pady=(2, 10))

    def _build_audio_tab(self) -> None:
        """音声・効果音に関する設定タブ"""
        frame = self.tab_audio
        
        tk.Label(frame, text="マスター音量:", font=("", 13), bg="#34495E", fg="white").pack(anchor="w", padx=30, pady=(30, 5))
        self.master_vol_slider = tk.Scale(frame, from_=0, to=100, orient="horizontal", bg="#34495E", fg="white", highlightbackground="#34495E", length=300)
        self.master_vol_slider.pack(anchor="w", padx=30)

        tk.Label(frame, text="SE (効果音) 音量:", font=("", 13), bg="#34495E", fg="white").pack(anchor="w", padx=30, pady=(20, 5))
        self.se_vol_slider = tk.Scale(frame, from_=0, to=100, orient="horizontal", bg="#34495E", fg="white", highlightbackground="#34495E", length=300)
        self.se_vol_slider.pack(anchor="w", padx=30)

    def _build_theme_tab(self) -> None:
        """外観・表示に関する設定タブ"""
        frame = self.tab_theme
        
        # UIカラーテーマ
        tk.Label(frame, text="UI カラーテーマ:", font=("", 13), bg="#34495E", fg="white").pack(anchor="w", padx=30, pady=(20, 5))
        self.theme_var = tk.StringVar(value="light")
        tk.Radiobutton(frame, text="ライトテーマ (温かみのある標準)", variable=self.theme_var, value="light", font=("", 11), bg="#34495E", fg="white", selectcolor="#2C3E50").pack(anchor="w", padx=50, pady=2)
        tk.Radiobutton(frame, text="ダークテーマ (目に優しい暗色)", variable=self.theme_var, value="dark", font=("", 11), bg="#34495E", fg="white", selectcolor="#2C3E50").pack(anchor="w", padx=50, pady=2)

        # 画面倍率 (UI Scale)
        tk.Label(frame, text="画面サイズ倍率 (UI Scale):", font=("", 13), bg="#34495E", fg="white").pack(anchor="w", padx=30, pady=(15, 5))
        self.ui_scale_var = tk.StringVar(value="1.0")
        scale_frame = tk.Frame(frame, bg="#34495E")
        scale_frame.pack(anchor="w", padx=50)
        for val in ["1.0", "1.25", "1.5"]:
            tk.Radiobutton(scale_frame, text=f"{val}倍", variable=self.ui_scale_var, value=val, font=("", 11), bg="#34495E", fg="white", selectcolor="#2C3E50").pack(side="left", padx=10)

        # フルスクリーン切替
        self.fullscreen_var = tk.BooleanVar(value=False)
        fs_check = tk.Checkbutton(
            frame, text="フルスクリーン表示にする", variable=self.fullscreen_var,
            font=("", 13), bg="#34495E", fg="white", selectcolor="#2C3E50", activebackground="#34495E", activeforeground="white"
        )
        fs_check.pack(anchor="w", padx=30, pady=(15, 5))

    def _build_system_tab(self) -> None:
        """システム・デバッグ設定タブ"""
        frame = self.tab_system

        # デバッグ情報の表示切替
        self.debug_mode_var = tk.BooleanVar(value=False)
        debug_check = tk.Checkbutton(
            frame, text="デバッグ情報（内部抽出タグ等の可視化）を表示する", variable=self.debug_mode_var,
            font=("", 13), bg="#34495E", fg="white", selectcolor="#2C3E50", activebackground="#34495E", activeforeground="white"
        )
        debug_check.pack(anchor="w", padx=30, pady=(30, 15))

        # お題データの強制リロードボタン
        reload_btn = tk.Button(
            frame, text="🔄 お題データを再読み込み (Reload Topics)", font=("", 12, "bold"),
            bg="#D35400", fg="white", command=self._reload_topics
        )
        reload_btn.pack(anchor="w", padx=30, pady=(5, 5))
        tk.Label(frame, text="※ data/topics.json などの変更をアプリ再起動なしで反映します。", font=("", 9), bg="#34495E", fg="#BDC3C7").pack(anchor="w", padx=30)

    def on_show(self, **kwargs) -> None:
        self.focus_set()
        self.status_label.config(text="")

        # 現在の設定値をフォームに反映
        self.idle_entry.delete(0, tk.END)
        self.idle_entry.insert(0, str(config.IDLE_TIMEOUT_SEC))

        self.max_attempt_entry.delete(0, tk.END)
        self.max_attempt_entry.insert(0, str(config.MAX_ATTEMPTS))

        self.enable_timer_var.set(getattr(config, "ENABLE_TIMER", True))
        self.time_limit_entry.delete(0, tk.END)
        self.time_limit_entry.insert(0, str(getattr(config, "TIME_LIMIT_SEC", 60)))

        delay_sec = getattr(config, "LOADING_DELAY_MS", 1500) / 1000.0
        self.loading_delay_entry.delete(0, tk.END)
        self.loading_delay_entry.insert(0, str(delay_sec))

        self.master_vol_slider.set(config.MASTER_VOLUME)
        self.se_vol_slider.set(config.SE_VOLUME)
        self.theme_var.set(config.THEME)

        self.ui_scale_var.set(str(getattr(config, "UI_SCALE", 1.0)))
        self.fullscreen_var.set(getattr(config, "IS_FULLSCREEN", False))
        self.debug_mode_var.set(getattr(config, "DEBUG_MODE", False))

    def _save_settings(self) -> None:
        try:
            new_idle = int(self.idle_entry.get())
            new_max = int(self.max_attempt_entry.get())
            new_time_limit = int(self.time_limit_entry.get())
            new_loading_sec = float(self.loading_delay_entry.get())
            
            if new_idle <= 0 or new_max <= 0 or new_time_limit <= 0 or new_loading_sec < 0:
                raise ValueError("正の数値を入力してください。")

            new_master = self.master_vol_slider.get()
            new_se = self.se_vol_slider.get()
            new_theme = self.theme_var.get()
            new_enable_timer = self.enable_timer_var.get()
            new_ui_scale = float(self.ui_scale_var.get())
            new_fullscreen = self.fullscreen_var.get()
            new_debug_mode = self.debug_mode_var.get()
            new_loading_ms = int(new_loading_sec * 1000)

            # config.py の save_config を呼び出して保存
            config.save_config(
                idle_sec=new_idle,
                max_attempts=new_max,
                master_vol=new_master,
                se_vol=new_se,
                theme=new_theme,
                enable_timer=new_enable_timer,
                time_limit_sec=new_time_limit,
                loading_delay_ms=new_loading_ms,
                ui_scale=new_ui_scale,
                is_fullscreen=new_fullscreen,
                debug_mode=new_debug_mode
            )

            # ーーー★ ここでGameControllerのapply_settings()を呼び出して即時反映させる ★ーーー
            if hasattr(self.controller, "apply_settings"):
                self.controller.apply_settings()

            # ログに残す
            self.logger.log_admin_change(new_idle, new_max)

            self.status_label.config(
                text="✔ 設定を正常に保存しました！", 
                fg="#2ECC71"
            )

        except ValueError as e:
            self.status_label.config(
                text=f"✖ 入力エラー: 正しい数値を入力してください ({e})", 
                fg="#E74C3C"
            )

    def _reload_topics(self) -> None:
        """お題データやリポジトリの強制再読み込みを行う"""
        try:
            if hasattr(self.controller, "topic_repo"):
                self.controller.topic_repo.load_topics()
            self.status_label.config(
                text="✔ お題データを正常に再読み込みしました！", 
                fg="#2ECC71"
            )
        except Exception as e:
            self.status_label.config(
                text=f"✖ 再読み込みに失敗しました: {e}", 
                fg="#E74C3C"
            )

    def _back_to_title(self) -> None:
        self.controller.next_scene("title")

    def _exit_app(self) -> None:
        from tkinter import messagebox
        if messagebox.askyesno("確認", "アプリケーションを終了しますか？"):
            self.logger.log_system("SHUTDOWN", "管理者画面から終了されました")
            self.controller.root.destroy()