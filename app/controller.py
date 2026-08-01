import tkinter as tk
from app.scenes.title_scene import TitleScene
from app.scenes.topic_scene import TopicScene
from app.scenes.input_scene import InputScene
from app.scenes.result_scene import ResultScene
from app.scenes.end_scene import EndScene
from app.scenes.loading_scene import LoadingScene
from app.scenes.admin_scene import AdminScene

from app.core.prompt_analyzer import PromptAnalyzer
from app.core.keyword_tag_mapper import KeywordTagMapper
from app.repository.image_repository import ImageRepository
from app.core.score_calculator import ScoreCalculator
from app.core.image_matcher import ImageMatcher
from app.repository.topic_repository import TopicRepository
from app.core.feedback_generator import FeedbackGenerator
from app.core.game_session import GameSession
from app.core.idle_timer import IdleTimer
from app.core.play_logger import PlayLogger  # 追加

# ーーー 追加：config.py から設定値をインポート ーーー
import config

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

        # ーーー 追加：プレイロガーの初期化 ーーー
        self.logger = PlayLogger()
        
        self.current_session = None
        
        # ーーー 変更：config.py の設定値（IDLE_TIMEOUT_SEC）を使用する ーーー
        self.idle_timer = IdleTimer(
            root=self.root, 
            timeout_sec=config.IDLE_TIMEOUT_SEC, 
            on_timeout=self.reset
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
        self.scenes["loading"] = LoadingScene(self.container, self)
        self.scenes["result"] = ResultScene(self.container, self)
        self.scenes["end"] = EndScene(self.container, self)

        # ーーー 追加：管理者画面の登録 ーーー
        self.scenes["admin"] = AdminScene(self.container, self)
        
        for scene in self.scenes.values():
            scene.grid(row=0, column=0, sticky="nsew")

    def start(self) -> None:
        self.next_scene("title")

    def start_new_session(self) -> None:
        """お題を選出し、新しいGameSessionを生成する[cite: 1]"""
        # ーーー 変更：ランダムにお題を1件選出する ーーー
        topic = self.topic_repo.get_random_topic()
        self.current_session = GameSession(topic)
        self.next_scene("topic", topic=topic)  # お題データを画面に渡す

    def next_scene(self, scene_name: str, **kwargs) -> None:
        if scene_name in self.scenes:
            scene = self.scenes[scene_name]
            scene.tkraise()
            scene.on_show(**kwargs)

    def handle_submit(self, prompt_text: str) -> None:
        self.next_scene("loading")
        self.root.update()
        
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
        is_finished = self.current_session.is_finished()

        # ーーー 追加：プレイログをCSVに書き込む ーーー
        self.logger.log_attempt(
            topic_id=current_topic.get("topic_id"),
            attempt_count=self.current_session.attempts,
            prompt=prompt_text,
            tags=tags,
            matched_image=best_img.get("file"),
            feedbacks=feedbacks
        )
        
        # ーーー 変更：config.py の設定値（LOADING_DELAY_MS）を使用する ーーー
        self.root.after(config.LOADING_DELAY_MS, lambda: self.next_scene(
            "result", 
            best_image=best_img, 
            feedbacks=feedbacks,
            is_finished=is_finished
        ))

    def reset(self) -> None:
        self.current_session = None
        self.next_scene("title")