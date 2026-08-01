import tkinter as tk
from app.scenes.base_scene import SceneBase

class InputScene(SceneBase):
    """プロンプト入力画面 (SC-03)[cite: 1]"""
    
    def __init__(self, parent: tk.Widget, controller) -> None:
        super().__init__(parent, controller)
        self.configure(bg="#FFF8E7")

        # 画面全体の中央に配置するためのコンテナ（weightを使って完全に中央へ寄せます）
        self.rowconfigure(0, weight=1)
        self.rowconfigure(2, weight=1)
        self.columnconfigure(0, weight=1)

        center_frame = tk.Frame(self, bg="#FFF8E7")
        center_frame.grid(row=1, column=0, sticky="nsew")
        center_frame.columnconfigure(0, weight=1)

        # I-01: フィードバック表示領域
        self.feedback_label = tk.Label(
            center_frame,
            text="", 
            font=("", 24),
            bg="#FFF8E7",
            fg="#FFB74D",
            wraplength=750,
            justify="center"
        )
        self.feedback_label.pack(pady=(0, 15))

        # 案内文
        tk.Label(
            center_frame, text="AIに伝える言葉を入力してね", font=("", 24), bg="#FFF8E7"
        ).pack(pady=10)

        # I-02: 自由記述入力欄
        self.entry_var = tk.StringVar()
        self.entry = tk.Entry(
            center_frame,
            textvariable=self.entry_var,
            font=("", 32),
            width=25,
            bd=3,
            relief="solid"
        )
        self.entry.pack(pady=15)

        # ボタンを配置するフレーム
        self.btn_frame = tk.Frame(center_frame, bg="#FFF8E7")
        self.btn_frame.pack(pady=15)

        # I-03: 送信ボタン
        self.submit_btn = tk.Button(
            self.btn_frame,
            text="送信する [Enter]",
            font=("", 22, "bold"),
            bg="#FF9800",
            fg="white",
            width=18,
            command=self._on_submit
        )
        self.submit_btn.pack(side="left", padx=10)

        # タイトルに戻るボタン (Escキー対応)
        self.back_btn = tk.Button(
            self.btn_frame,
            text="やめる [Esc]",
            font=("", 22, "bold"),
            bg="#9e9e9e",
            fg="white",
            width=12,
            command=self._on_back_to_title
        )
        self.back_btn.pack(side="left", padx=10)

    def on_show(self, **kwargs) -> None:
        self.entry_var.set("")
        self.entry.focus_set()
        
        self.entry.bind("<Return>", lambda e: self._on_submit())
        self.bind_all("<Escape>", lambda e: self._on_back_to_title())

    def on_hide(self) -> None:
        try:
            self.unbind_all("<Escape>")
        except Exception:
            pass

    def _on_submit(self):
        input_text = self.entry_var.get().strip()
        if not input_text:
            self.feedback_label.config(text="なにか書いてみてね！")
            return
            
        self.on_hide()
        self.controller.handle_submit(input_text)

    def _on_back_to_title(self):
        self.on_hide()
        self.controller.reset()