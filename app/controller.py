import tkinter as tk
from app.scenes.title_scene import TitleScene
from app.scenes.topic_scene import TopicScene
from app.scenes.input_scene import InputScene
# ーーー 追加：結果画面 ーーー
from app.scenes.result_scene import ResultScene

from app.core.prompt_analyzer import PromptAnalyzer
from app.core.keyword_tag_mapper import KeywordTagMapper
from app.repository.image_repository import ImageRepository
from app.core.score_calculator import ScoreCalculator
from app.core.image_matcher import ImageMatcher
# ーーー 追加：お題とフィードバックのクラス ーーー
from app.repository.topic_repository import TopicRepository
from app.core.feedback_generator import FeedbackGenerator


class GameController:
    """画面遷移とゲーム全体の進行を統括する[cite: 1]"""
    
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        
        # 1. 準備
        self.analyzer = PromptAnalyzer()
        self.tag_mapper = KeywordTagMapper(
            synonyms_path="data/synonyms.json",
            map_path="data/keyword_tag_map.json"
        )
        self.image_repo = ImageRepository(tags_path="data/tags.json")
        self.score_calc = ScoreCalculator()
        self.image_matcher = ImageMatcher(
            images_data=self.image_repo.load_all(),
            calculator=self.score_calc
        )
        
        # ーーー 追加：お題とフィードバックの準備 ーーー
        self.topic_repo = TopicRepository(topics_path="data/topics.json")
        self.feedback_gen = FeedbackGenerator(messages_path="data/feedback_messages.json")
        
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
        self.scenes["result"] = ResultScene(self.container, self)  # 追加
        
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
        # 解析〜画像マッチング
        keywords = self.analyzer.extract_keywords(prompt_text)
        tags = self.tag_mapper.map_to_tags(keywords)
        match_result = self.image_matcher.find_best_match(tags)
        best_img = match_result["best_image"]
        
        # ーーー 追加：フィードバック生成と結果画面への遷移 ーーー
        # 現在のお題を取得（テスト用に1つ目固定）
        current_topic = self.topic_repo.get_topic(0)
        
        # お題の正解と、入力されたタグを比較してフィードバックを作る
        feedbacks = self.feedback_gen.generate(
            required_tags=current_topic["required_tags"], 
            input_tags=tags
        )
        
        # 結果画面にデータを渡して遷移
        self.next_scene("result", best_image=best_img, feedbacks=feedbacks)