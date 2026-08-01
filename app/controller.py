import tkinter as tk
from app.scenes.title_scene import TitleScene
from app.scenes.topic_scene import TopicScene
from app.scenes.input_scene import InputScene

# ーーー 追加：解析クラスのインポート ーーー
from app.core.prompt_analyzer import PromptAnalyzer
from app.core.keyword_tag_mapper import KeywordTagMapper

class GameController:
    """画面遷移とゲーム全体の進行を統括する[cite: 1]"""
    
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        
        # ーーー 追加：解析クラスの準備 ーーー
        self.analyzer = PromptAnalyzer()
        self.tag_mapper = KeywordTagMapper(
            synonyms_path="data/synonyms.json",
            map_path="data/keyword_tag_map.json"
        )
        
        self.container = tk.Frame(self.root)
        self.container.pack(fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)
        
        self.scenes = {}
        self._setup_scenes()

    def _setup_scenes(self) -> None:
        self.scenes["title"] = TitleScene(self.container, self)
        self.scenes["topic"] = TopicScene(self.container, self)
        self.scenes["input"] = InputScene(self.container, self)
        
        for scene in self.scenes.values():
            scene.grid(row=0, column=0, sticky="nsew")

    def start(self) -> None:
        self.next_scene("title")

    def next_scene(self, scene_name: str, **kwargs) -> None:
        if scene_name in self.scenes:
            scene = self.scenes[scene_name]
            scene.tkraise()
            scene.on_show(**kwargs)

    # ーーー 追加：送信ボタンが押された時の処理 (F-04, F-05)[cite: 1] ーーー
    def handle_submit(self, prompt_text: str) -> None:
        print(f"\n--- 処理開始 ---")
        print(f"入力文: {prompt_text}")
        
        # 1. 文章から単語（キーワード）を抽出[cite: 1]
        keywords = self.analyzer.extract_keywords(prompt_text)
        print(f"抽出されたキーワード: {keywords}")
        
        # 2. 単語をタグに変換[cite: 1]
        tags = self.tag_mapper.map_to_tags(keywords)
        print(f"変換されたタグ: {tags}")
        print(f"--- 処理完了 ---\n")