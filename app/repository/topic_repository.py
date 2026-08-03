import json
import random

class TopicRepository:
    """topics.jsonのロードとお題選出を行う"""
    
    def __init__(self, topics_path: str = "data/topics.json") -> None:
        self.topics_path = topics_path
        self.topics = []
        self.last_topic_id = None
        self.load_topics()  # 初期化時に読み込みを実行

    def load_topics(self) -> None:
        """JSONファイルからお題データを再読み込みする（ホットリロード用）"""
        try:
            with open(self.topics_path, 'r', encoding='utf-8') as f:
                self.topics = json.load(f)
        except Exception as e:
            print(f"お題データのロードに失敗しました ({self.topics_path}): {e}")
            if not self.topics:
                self.topics = []

    def load_all(self) -> list[dict]:
        return self.topics

    def get_random_topic(self) -> dict:
        """直近出題したお題を除外しつつランダムに1件選出する"""
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