from app.core.score_calculator import ScoreCalculator

class ImageMatcher:
    """タグ集合と画像DBを照合し最良の一致画像を検索する[cite: 1]"""
    
    def __init__(self, images_data: list[dict], calculator: ScoreCalculator) -> None:
        self.images = images_data
        self.calculator = calculator

    def find_best_match(self, input_tags: dict[str, str]) -> dict:
        """全画像に対しスコアを計算し、最高スコアの画像を返す[cite: 1]"""
        scored_images = []
        
        for img in self.images:
            # 各画像のスコアを計算
            score = self.calculator.calculate(input_tags, img["tags"])
            scored_images.append((score, img))

        # スコア降順(マイナスをつけて降順化)、同点の場合は画像ID(img["id"])昇順でソート[cite: 1]
        scored_images.sort(key=lambda x: (-x[0], x[1]["id"]))
        
        # 最高得点の画像とスコアを返す
        best_score, best_image = scored_images[0]
        return {
            "best_image": best_image,
            "score": best_score
        }