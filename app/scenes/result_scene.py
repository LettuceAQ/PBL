import tkinter as tk
from app.scenes.base_scene import SceneBase

class ResultScene(SceneBase):
    """結果／フィードバック画面 (SC-05)[cite: 1]"""
    
    def __init__(self, parent: tk.Widget, controller) -> None:
        super().__init__(parent, controller)
        self.configure(bg="#FFF8E7")

        # R-01: 選出画像表示領域（仮）[cite: 1]
        self.image_label = tk.Label(
            self, 
            text="[ここに選ばれた画像が出ます]", 
            font=("", 24), 
            bg="lightgray", 
            width=40, height=8 
        )
        self.image_label.pack(pady=(20, 10))

        # R-03: フィードバック文表示領域[cite: 1]
        self.feedback_label = tk.Label(
            self, 
            text="", 
            font=("", 24, "bold"), 
            bg="#FFF8E7", 
            fg="#FFB74D",
            wraplength=750,  
            justify="center"
        )
        self.feedback_label.pack(pady=10)

        # R-04, R-05: ボタンを横に並べるためのフレーム[cite: 1]
        self.btn_frame = tk.Frame(self, bg="#FFF8E7")
        self.btn_frame.pack(pady=(10, 20))

        # R-04: もう一度挑戦するボタン[cite: 1]
        self.retry_btn = tk.Button(
            self.btn_frame, 
            text="もう一度挑戦する", 
            font=("", 24, "bold"),
            bg="#29B6F6", 
            fg="white", 
            width=20,
            command=self._on_retry
        )
        self.retry_btn.pack(side="left", padx=10)
        
        # R-05: おわる（終了する）ボタン[cite: 1]
        self.end_btn = tk.Button(
            self.btn_frame, 
            text="次へ（おわる）", 
            font=("", 24, "bold"),
            bg="#FF9800", 
            fg="white", 
            width=20,
            command=self._on_end
        )
        # ※ ここではpack()しません。on_showメソッドの中で条件に応じて表示させます。

    def on_show(self, **kwargs) -> None:
        """画面表示時の処理。コントローラーから結果データを受け取る"""
        best_img = kwargs.get("best_image", {})
        feedbacks = kwargs.get("feedbacks", [])
        is_finished = kwargs.get("is_finished", False)
        
        # 画像IDの表示
        img_id = best_img.get("id", "不明な画像")
        self.image_label.config(text=f"[ AIが選んだ画像: {img_id} ]")
        
        # フィードバックのリストを改行でつないで表示
        feedback_text = "\n\n".join(feedbacks)
        self.feedback_label.config(text=feedback_text)
        
        # 終了状態（3回目に到達したか）に応じてボタンを出し分ける
        if is_finished:
            # 3回終わっていたらリトライボタンを消して、次へボタンを出す
            self.retry_btn.pack_forget()
            self.end_btn.pack(side="left", padx=10)
        else:
            # まだ挑戦できる場合はリトライボタンを出し、次へボタンを消す
            self.end_btn.pack_forget()
            self.retry_btn.pack(side="left", padx=10)

    def _on_retry(self):
        """もう一度挑戦するボタンが押されたとき"""
        self.controller.next_scene("input")
        
    def _on_end(self):
        """次へボタンが押されたとき"""
        self.controller.next_scene("end")