import re
import json
import unicodedata
from janome.tokenizer import Tokenizer

class PromptAnalyzer:
    """入力文字列の正規化と形態素解析によるキーワード抽出を行う[cite: 1]"""
    
    def __init__(self, synonyms_path: str = "data/synonyms.json") -> None:
        self.tokenizer = Tokenizer()
        
        # ーーー 追加：同義語辞書を読み込む ーーー
        with open(synonyms_path, 'r', encoding='utf-8') as f:
            self.synonyms = json.load(f)

    def normalize(self, text: str) -> str:
        """全角/半角統一・記号除去・事前の表記ゆれ吸収を行う[cite: 1]"""
        text = unicodedata.normalize('NFKC', text)
        text = re.sub(r'[^\w\sぁ-んァ-ン一-龥]', '', text)
        
        # ーーー 追加：Janomeが分解してしまう前に、文章の段階で代表語に置き換える ーーー
        for representative, variants in self.synonyms.items():
            for variant in variants:
                text = text.replace(variant, representative)
                
        return text

    def extract_keywords(self, text: str) -> list[str]:
        """形態素解析で名詞・形容詞を抽出する[cite: 1]"""
        text = self.normalize(text)
        keywords = []
        
        for token in self.tokenizer.tokenize(text):
            part_of_speech = token.part_of_speech.split(',')[0]
            if part_of_speech in ['名詞', '形容詞']:
                keywords.append(token.base_form)
                
        return keywords