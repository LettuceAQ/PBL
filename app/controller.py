import tkinter as tk
from app.scenes.title_scene import TitleScene
from app.scenes.topic_scene import TopicScene    # 追加
from app.scenes.input_scene import InputScene    # 追加

class GameController:
    """画面遷移とゲーム全体の進行を統括する[cite: 1]"""
    
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        
        self.container = tk.Frame(self.root)
        self.container.pack(fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)
        
        self.scenes = {}
        self._setup_scenes()

    def _setup_scenes(self) -> None:
        """必要な画面をインスタンス化して辞書に格納する"""
        self.scenes["title"] = TitleScene(self.container, self)
        self.scenes["topic"] = TopicScene(self.container, self)  # 追加
        self.scenes["input"] = InputScene(self.container, self)  # 追加
        
        for scene in self.scenes.values():
            scene.grid(row=0, column=0, sticky="nsew")

    def start(self) -> None:
        self.next_scene("title")

    def next_scene(self, scene_name: str, **kwargs) -> None:
        if scene_name in self.scenes:
            scene = self.scenes[scene_name]
            scene.tkraise()
            scene.on_show(**kwargs)