import json

class ImageRepository:
    """tags.jsonのロード・キャッシュを行う"""
    
    def __init__(self, tags_path: str = "data/tags.json") -> None:
        with open(tags_path, 'r', encoding='utf-8') as f:
            self.images_data = json.load(f)

    def load_all(self) -> list[dict]:
        """全件ロードする"""
        return self.images_data