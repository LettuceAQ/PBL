import os
import csv
import json
import sys
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
from app.core.play_logger import PlayLogger

import config

class GameController:
    """画面遷移とゲーム全体の進行を統括する"""
    
    def __init__(self, root: tk.Tk) -> None:
        self.root = root

        # 起動時に設定（フルスクリーンや画面倍率）を適用
        self.apply_settings()

        # 実行ファイルの場所（または起動時のカレントディレクトリ）を基準にする
        if getattr(sys, 'frozen', False):
            base_dir = os.path.dirname(sys.executable)
        else:
            base_dir = os.getcwd()

        synonyms_path = os.path.join(base_dir, "data", "synonyms.json")
        map_path = os.path.join(base_dir, "data", "keyword_tag_map.json")
        tags_path = os.path.join(base_dir, "data", "tags.json")
        topics_path = os.path.join(base_dir, "data", "topics.json")
        feedback_path = os.path.join(base_dir, "data", "feedback_messages.json")

        self.analyzer = PromptAnalyzer()
        self.tag_mapper = KeywordTagMapper(
            synonyms_path=synonyms_path,
            map_path=map_path
        )
        self.image_repo = ImageRepository(tags_path=tags_path)
        self.score_calc = ScoreCalculator()
        self.image_matcher = ImageMatcher(
            images_data=self.image_repo.load_all(),
            calculator=self.score_calc
        )
        self.topic_repo = TopicRepository(topics_path=topics_path)
        self.feedback_gen = FeedbackGenerator(messages_path=feedback_path)

        # プレイロガーの初期化
        log_dir = os.path.join(base_dir, "logs")
        self.logger = PlayLogger()
        
        self.current_session = None
        
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
        self.scenes["admin"] = AdminScene(self.container, self)
        
        for scene in self.scenes.values():
            scene.grid(row=0, column=0, sticky="nsew")

    def start(self) -> None:
        self.next_scene("title")

    def start_new_session(self) -> None:
        """お題を選出し、新しいGameSessionを生成する"""
        topic = self.topic_repo.get_random_topic()
        self.current_session = GameSession(topic)
        self.next_scene("topic", topic=topic)

    def next_scene(self, scene_name: str, **kwargs) -> None:
        if scene_name in self.scenes:
            scene = self.scenes[scene_name]
            scene.tkraise()
            scene.on_show(**kwargs)

    def handle_submit(self, prompt_text: str) -> None:
        try:
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

            # プレイログをCSVに書き込む
            self.logger.log_attempt(
                topic_id=current_topic.get("topic_id"),
                attempt_count=self.current_session.attempts,
                prompt=prompt_text,
                tags=tags,
                matched_image=best_img.get("file"),
                feedbacks=feedbacks
            )
            
            self.root.after(config.LOADING_DELAY_MS, lambda: self.next_scene(
                "result", 
                best_image=best_img, 
                feedbacks=feedbacks,
                is_finished=is_finished
            ))

        except Exception as e:
            # 予期せぬエラーが発生した場合のキャッチとログ記録
            import traceback
            error_detail = traceback.format_exc()
            self.logger.log_error("GameController.handle_submit", str(e) + "\n" + error_detail)
            print(f"エラーが発生しました: {e}")
            
            # 安全のため、エラー時はタイトル画面に戻す
            self.reset()

    def apply_settings(self) -> None:
        """config.pyの設定内容をウィンドウ全体に適用する"""
        # 1. フルスクリーン状態の適用
        self.root.attributes("-fullscreen", config.IS_FULLSCREEN)
        
        if not config.IS_FULLSCREEN:
            # ウィンドウモードの場合、UI Scale に応じてウィンドウサイズをスケーリング
            base_w = getattr(config, "BASE_WINDOW_WIDTH", 800)
            base_h = getattr(config, "BASE_WINDOW_HEIGHT", 600)
            
            scaled_w = int(base_w * config.UI_SCALE)
            scaled_h = int(base_h * config.UI_SCALE)
            
            self.root.geometry(f"{scaled_w}x{scaled_h}")

        # 2. Tkinter全体のスケーリング倍率（UI Scale）を反映
        try:
            self.root.tk.call('tk', 'scaling', 1.0 * config.UI_SCALE)
        except Exception:
            pass

    def reset(self) -> None:
        self.current_session = None
        self.next_scene("title")