import os
from PIL import Image, ImageDraw, ImageFont

# 画像保存先フォルダの確認・作成
os.makedirs("data/images", exist_ok=True)

# 作り出す画像のデータ（tags.json に合わせた3枚）
dummy_data = [
    {"file": "img_0001.png", "bg_color": "brown", "text": "茶色い犬\n(赤い帽子)"},
    {"file": "img_0002.png", "bg_color": "white", "text": "白い猫\n(青いリボン, 部屋)"},
    {"file": "img_0003.png", "bg_color": "lightgreen", "text": "白い犬\n(公園)"},
]

for data in dummy_data:
    # 400x400 の画像を作成
    img = Image.new("RGB", (400, 400), color=data["bg_color"])
    draw = ImageDraw.Draw(img)
    
    # 中央に文字を描画（フォント指定なしのデフォルトフォント）
    draw.text((100, 180), data["text"], fill="black", align="center")
    
    # 保存
    save_path = f"data/images/{data['file']}"
    img.save(save_path)
    print(f"作成完了: {save_path}")