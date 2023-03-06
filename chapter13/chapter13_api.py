import torch
from fastapi import FastAPI, File, UploadFile
from PIL import Image
from pydantic import BaseModel
from transformers import AutoImageProcessor, AutoModelForObjectDetection


class Object(BaseModel):
    box: tuple[float, float, float, float]
    label: str


class Objects(BaseModel):
    objects: list[Object]


class ObjectDetection:
    image_processor: AutoImageProcessor | None = None
    model: AutoModelForObjectDetection | None = None

    def load_model(self) -> None:
        """Loads the model"""
        self.image_processor = AutoImageProcessor.from_pretrained("hustvl/yolos-tiny")
        self.model = AutoModelForObjectDetection.from_pretrained("hustvl/yolos-tiny")

    def predict(self, image: Image.Image) -> Objects:
        """Runs a prediction"""
        if not self.image_processor or not self.model:
            raise RuntimeError("Model is not loaded")
        inputs = self.image_processor(images=image, return_tensors="pt")
        outputs = self.model(**inputs)

        target_sizes = torch.tensor([image.size[::-1]])
        results = self.image_processor.post_process_object_detection(
            outputs, threshold=0.7, target_sizes=target_sizes
        )[0]

        objects: list[Object] = []
        for score, label, box in zip(
            results["scores"], results["labels"], results["boxes"]
        ):
            if score > 0.7:
                box_values = box.tolist()
                label = self.model.config.id2label[label.item()]
                objects.append(Object(box=box_values, label=label))
        return Objects(objects=objects)


app = FastAPI()
object_detection = ObjectDetection()


@app.post("/object-detection", response_model=Objects)
async def post_object_detection(image: UploadFile = File(...)) -> Objects:
    image_object = Image.open(image.file)
    return object_detection.predict(image_object)


@app.on_event("startup")
async def startup():
    object_detection.load_model()
