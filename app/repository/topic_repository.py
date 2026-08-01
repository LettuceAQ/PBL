import json
import random

class TopicRepository:
    """topics.jsonのロードとお題選出を行う"""
    
    def __init__(self, topics_path: str = "data/topics.json") -> None:
        with open(topics_path, 'r', encoding='utf-8') as f:
            self.topics = json.load(f)
        self.last_topic_id = None

    def load_all(self) -> list[dict]:
        return self.topics

    def get_random_topic(self) -> dict:
        """直近出題したお題を除外しつつランダムに1件選出する[cite: 1]"""
        if not self.topics:
            raise ValueError("お題データが登録されていません。")
            
        # 1件しかない場合はそのまま返す
        if len(self.topics) == 1:
            return self.topics[0]
            
        # 直近と違うお題になるまでループ
        while True:
            topic = random.choice(self.topics)
            if topic["topic_id"] != self.last_topic_id:
                self.last_topic_id = topic["topic_id"]
                return topic