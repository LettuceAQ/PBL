import json

class KeywordTagMapper:
    """キーワードを同義語辞書経由でタグへ変換する[cite: 1]"""
    
    def __init__(self, synonyms_path: str, map_path: str) -> None:
        # 起動時にJSONファイルを読み込む[cite: 1]
        with open(synonyms_path, 'r', encoding='utf-8') as f:
            self.synonyms = json.load(f)
            
        with open(map_path, 'r', encoding='utf-8') as f:
            self.keyword_tag_map = json.load(f)

    def resolve_synonym(self, keyword: str) -> str:
        """表記ゆれを代表語に正規化する[cite: 1]"""
        # 辞書を順番に見て、該当する揺れがあれば代表語（キー）を返す
        for representative, variants in self.synonyms.items():
            if keyword in variants or keyword == representative:
                return representative
        return keyword

    def map_to_tags(self, keywords: list[str]) -> dict[str, str]:
        """キーワード列からタグ辞書を生成する[cite: 1]"""
        tags = {}
        for kw in keywords:
            # 揺れを吸収（例：「わんこ」→「犬」）
            resolved = self.resolve_synonym(kw)
            
            # タグ変換マップに存在すればタグに追加
            if resolved in self.keyword_tag_map:
                tag_info = self.keyword_tag_map[resolved]
                category = tag_info["category"]
                value = tag_info["value"]
                
                # 同一カテゴリが出た場合は後から出たもので上書き[cite: 1]
                tags[category] = value 
                
        return tags