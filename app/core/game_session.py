import config

class GameSession:
    """1プレイ分の状態（試行回数・現在のお題）を保持する[cite: 1]"""
    
    def __init__(self, topic: dict) -> None:
        self.topic = topic
        self.attempts = 0  # 現在の挑戦回数
        
    def add_attempt(self) -> None:
        """試行回数を1増やす[cite: 1]"""
        self.attempts += 1
        
    def is_finished(self) -> bool:
        """最大試行回数に到達したか判定する[cite: 1]"""
        # config.py から設定値を読み込む
        return self.attempts >= config.MAX_ATTEMPTS
        
    def attempts_left(self) -> int:
        """残りの試行回数を返す[cite: 1]"""
        return config.MAX_ATTEMPTS - self.attempts