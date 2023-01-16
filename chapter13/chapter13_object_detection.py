from pathlib import Path

import torch
from PIL import Image, ImageDraw
from transformers import YolosFeatureExtractor, YolosForObjectDetection

root_directory = Path(__file__).parent.parent
picture_path = root_directory / "assets" / "coffee-shop.jpg"
image = Image.open(picture_path)

feature_extractor = YolosFeatureExtractor.from_pretrained("hustvl/yolos-tiny")
model = YolosForObjectDetection.from_pretrained("hustvl/yolos-tiny")

inputs = feature_extractor(images=image, return_tensors="pt")
outputs = model(**inputs)

target_sizes = torch.tensor([image.size[::-1]])
results = feature_extractor.post_process(outputs, target_sizes=target_sizes)[0]

draw = ImageDraw.Draw(image)
for score, label, box in zip(results["scores"], results["labels"], results["boxes"]):
    if score > 0.7:
        box_values = box.tolist()
        label = model.config.id2label[label.item()]
        draw.rectangle(box_values, outline="green")
        draw.text(box_values[0:2], label, fill="green")
image.show()
