import random

from fastapi import FastAPI
from prometheus_client import Counter
from prometheus_fastapi_instrumentator import Instrumentator, metrics

app = FastAPI()

DICE_COUNTER = Counter(
    "app_dice_rolls_total",
    "Total number of dice rolls labelled per face",
    labelnames=["face"],
)


def roll_dice() -> int:
    result = random.randint(1, 6)
    DICE_COUNTER.labels(result).inc()
    return result


@app.get("/roll")
async def roll():
    return {"result": roll_dice()}


instrumentator = Instrumentator()
instrumentator.add(metrics.default())
instrumentator.instrument(app).expose(app)
