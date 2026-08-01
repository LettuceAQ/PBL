import json

class FeedbackGenerator:
    """お題の必須タグと入力タグの差分からフィードバック文を生成する[cite: 1]"""
    
    def __init__(self, messages_path: str = "data/feedback_messages.json") -> None:
        with open(messages_path, 'r', encoding='utf-8') as f:
            self.messages = json.load(f)
            
        # 優先してフィードバックを出すための重み（要件定義書準拠）[cite: 1, 2]
        self.weights = {"animal": 5, "item": 3, "item_color": 2, "color": 2, "background": 1}

    def generate(self, required_tags: dict[str, str], input_tags: dict[str, str]) -> list[str]:
        missing_tags = []
        
        # 必須タグが入力タグに含まれているか（一致しているか）チェック
        for category, required_value in required_tags.items():
            if input_tags.get(category) != required_value:
                missing_tags.append(category)
                
        # 不足タグを重みの大きい（重要度が高い）順に並び替え[cite: 1]
        missing_tags.sort(key=lambda c: self.weights.get(c, 0), reverse=True)
        
        feedbacks = []
        # 最大2件までフィードバック文を生成[cite: 1]
        for category in missing_tags[:2]:
            key = f"{category}:missing"
            if key in self.messages:
                feedbacks.append(self.messages[key])
                
        # 不足タグが0件（完全一致）の場合
        if not feedbacks:
            return ["ばっちり伝わったよ！大成功！"]
            
        return feedbacks