import tkinter as tk
from typing import Callable

class IdleTimer:
    """無操作状態を監視し、タイムアウト時にコールバックを発火する[cite: 1]"""
    
    def __init__(self, root: tk.Tk, timeout_sec: int, on_timeout: Callable[[], None]) -> None:
        self.root = root
        self.timeout_ms = timeout_sec * 1000  # ミリ秒に変換
        self.on_timeout_callback = on_timeout
        self.timer_id = None
        
        # 監視を開始
        self.reset()
        
        # ウィンドウ上のあらゆるキー入力・マウスクリックを監視してタイマーをリセットする
        self.root.bind_all("<Any-KeyPress>", self._on_activity, add="+")
        self.root.bind_all("<Any-Button>", self._on_activity, add="+")

    def _on_activity(self, event=None) -> None:
        """何らかの操作があった場合にタイマーをリセットする"""
        self.reset()

    def reset(self) -> None:
        """タイマーを再始動する[cite: 1]"""
        # 前のタイマーが動いていたらキャンセルする
        if self.timer_id is not None:
            self.root.after_cancel(self.timer_id)
            
        # 指定時間後にタイムアウト処理を実行するよう予約する
        self.timer_id = self.root.after(self.timeout_ms, self._handle_timeout)

    def _handle_timeout(self) -> None:
        """タイムアウト時に呼ばれる処理"""
        self.timer_id = None
        self.on_timeout_callback()

    def stop(self) -> None:
        """タイマーを完全に停止する（アプリ終了時などに使用）[cite: 1]"""
        if self.timer_id is not None:
            self.root.after_cancel(self.timer_id)
            self.timer_id = None