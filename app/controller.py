import tkinter as tk
from app.scenes.title_scene import TitleScene
from app.scenes.topic_scene import TopicScene
from app.scenes.input_scene import InputScene

from app.core.prompt_analyzer import PromptAnalyzer
from app.core.keyword_tag_mapper import KeywordTagMapper
# ーーー 追加：リポジトリと判定クラスのインポート ーーー
from app.repository.image_repository import ImageRepository
from app.core.score_calculator import ScoreCalculator
from app.core.image_matcher import ImageMatcher

class GameController:
    """画面遷移とゲーム全体の進行を統括する[cite: 1]"""
    
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        
        # 1. 解析クラスの準備
        self.analyzer = PromptAnalyzer()
        self.tag_mapper = KeywordTagMapper(
            synonyms_path="data/synonyms.json",
            map_path="data/keyword_tag_map.json"
        )
        
        # ーーー 追加：2. データと判定クラスの準備 ーーー
        self.image_repo = ImageRepository(tags_path="data/tags.json")
        self.score_calc = ScoreCalculator()
        self.image_matcher = ImageMatcher(
            images_data=self.image_repo.load_all(),
            calculator=self.score_calc
        )
        
        # 画面構築
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

    def handle_submit(self, prompt_text: str) -> None:
        print(f"\n--- 処理開始 ---")
        print(f"入力文: {prompt_text}")
        
        # 単語抽出とタグ変換
        keywords = self.analyzer.extract_keywords(prompt_text)
        tags = self.tag_mapper.map_to_tags(keywords)
        print(f"変換されたタグ: {tags}")
        
        # ーーー 追加：画像マッチングの実行 ーーー
        match_result = self.image_matcher.find_best_match(tags)
        best_img = match_result["best_image"]
        score = match_result["score"]
        
        print(f"選ばれた画像ID: {best_img['id']}")
        print(f"スコア: {score}点")
        print(f"画像が持っているタグ: {best_img['tags']}")
        print(f"--- 処理完了 ---\n")