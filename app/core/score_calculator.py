class ScoreCalculator:
    """カテゴリ別重み付けによる一致スコアを算出する[cite: 1]"""
    
    def __init__(self) -> None:
        # 重みの定義 (要件定義書 16.2)[cite: 2]
        self.weights = {
            "animal": 5,
            "item": 3,
            "item_color": 2,
            "color": 2,
            "background": 1
        }

    def calculate(self, input_tags: dict[str, str], image_tags: dict[str, str]) -> int:
        """一致したカテゴリの重みを合算してスコアを返す[cite: 1]"""
        score = 0
        for category, weight in self.weights.items():
            # 入力タグと画像タグの両方にそのカテゴリがあり、かつ値が一致していれば加点
            if category in input_tags and input_tags.get(category) == image_tags.get(category):
                score += weight
        return score