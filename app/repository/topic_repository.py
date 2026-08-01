import json

class TopicRepository:
    """topics.jsonのロードとお題選出を行う"""
    
    def __init__(self, topics_path: str = "data/topics.json") -> None:
        with open(topics_path, 'r', encoding='utf-8') as f:
            self.topics = json.load(f)

    def get_topic(self, index: int = 0) -> dict:
        """指定したお題（今回はテスト用なので常に最初の1件）を返す"""
        return self.topics[index]