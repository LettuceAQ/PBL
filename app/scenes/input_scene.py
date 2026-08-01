import tkinter as tk
from app.scenes.base_scene import SceneBase

class InputScene(SceneBase):
    """プロンプト入力画面 (SC-03)[cite: 1]"""
    
    def __init__(self, parent: tk.Widget, controller) -> None:
        super().__init__(parent, controller)
        self.configure(bg="#FFF8E7")

        # I-01: フィードバック表示領域
        self.feedback_label = tk.Label(
            self,
            text="", 
            font=("", 24),
            bg="#FFF8E7",
            fg="#FFB74D"
        )
        self.feedback_label.pack(pady=(40, 20))

        # 案内文
        tk.Label(
            self, text="AIに伝える言葉を入力してね", font=("", 24), bg="#FFF8E7"
        ).pack(pady=10)

        # I-02: 自由記述入力欄
        self.entry_var = tk.StringVar()
        self.entry = tk.Entry(
            self,
            textvariable=self.entry_var,
            font=("", 32),
            width=25,
            bd=3,
            relief="solid"
        )
        self.entry.pack(pady=20)

        # I-03: 送信ボタン
        self.submit_btn = tk.Button(
            self,
            text="送信する (Enter)",
            font=("", 28, "bold"),
            bg="#FF9800",
            fg="white",
            width=15,
            command=self._on_submit
        )
        self.submit_btn.pack(pady=30)

    def on_show(self, **kwargs) -> None:
        # 画面が表示されたら入力欄を空にして、すぐに入力できるようにフォーカスを当てる
        self.entry_var.set("")
        self.entry.focus_set()
        
        # ーーー 修正箇所 ーーー
        # self (画面全体) ではなく、self.entry (入力欄自体) にEnterキーを紐付ける
        self.entry.bind("<Return>", lambda e: self._on_submit())

    def _on_submit(self):
        # 入力された文字を取得
        input_text = self.entry_var.get().strip()
        
        if not input_text:
            self.feedback_label.config(text="なにか書いてみてね！")
            return
            
        # コントローラーに解析処理をお願いする
        self.controller.handle_submit(input_text)
        
        self.feedback_label.config(text="ターミナルを確認してください！")