import tkinter as tk
from app.scenes.title_scene import TitleScene
from app.scenes.topic_scene import TopicScene
from app.scenes.input_scene import InputScene
from app.scenes.result_scene import ResultScene
# ーーー 追加：終了画面 ーーー
from app.scenes.end_scene import EndScene

from app.core.prompt_analyzer import PromptAnalyzer
from app.core.keyword_tag_mapper import KeywordTagMapper
from app.repository.image_repository import ImageRepository
from app.core.score_calculator import ScoreCalculator
from app.core.image_matcher import ImageMatcher
from app.repository.topic_repository import TopicRepository
from app.core.feedback_generator import FeedbackGenerator
# ーーー 追加：ゲームセッション ーーー
from app.core.game_session import GameSession

class GameController:
    """画面遷移とゲーム全体の進行を統括する[cite: 1]"""
    
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        
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
        self.topic_repo = TopicRepository(topics_path="data/topics.json")
        self.feedback_gen = FeedbackGenerator(messages_path="data/feedback_messages.json")
        
        # ーーー 追加：現在進行中のセッションを保存する変数 ーーー
        self.current_session = None
        
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
        self.scenes["result"] = ResultScene(self.container, self)
        self.scenes["end"] = EndScene(self.container, self)  # 追加
        
        for scene in self.scenes.values():
            scene.grid(row=0, column=0, sticky="nsew")

    def start(self) -> None:
        self.next_scene("title")

    # ーーー 変更：タイトルからお題へ進む前にセッションを開始する ーーー
    def start_new_session(self) -> None:
        """お題を選出し、新しいGameSessionを生成する[cite: 1]"""
        # 今回はテストなので1番目のお題を固定で取得します
        topic = self.topic_repo.get_topic(0)
        self.current_session = GameSession(topic)
        self.next_scene("topic")

    def next_scene(self, scene_name: str, **kwargs) -> None:
        if scene_name in self.scenes:
            scene = self.scenes[scene_name]
            scene.tkraise()
            scene.on_show(**kwargs)

    def handle_submit(self, prompt_text: str) -> None:
        # 挑戦回数を1増やす
        self.current_session.add_attempt()
        
        keywords = self.analyzer.extract_keywords(prompt_text)
        tags = self.tag_mapper.map_to_tags(keywords)
        match_result = self.image_matcher.find_best_match(tags)
        best_img = match_result["best_image"]
        
        current_topic = self.current_session.topic
        
        feedbacks = self.feedback_gen.generate(
            required_tags=current_topic["required_tags"], 
            input_tags=tags
        )
        
        # 終了条件（3回終わったか）を結果画面に渡す
        is_finished = self.current_session.is_finished()
        
        self.next_scene(
            "result", 
            best_image=best_img, 
            feedbacks=feedbacks,
            is_finished=is_finished # 追加
        )

    # ーーー 追加：終了画面からタイトルへ戻る（リセット） ーーー
    def reset(self) -> None:
        """現在のセッションを破棄し、タイトル画面へ戻す[cite: 1]"""
        self.current_session = None
        self.next_scene("title")