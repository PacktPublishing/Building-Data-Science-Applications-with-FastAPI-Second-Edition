import random
import time

import dramatiq
from dramatiq.brokers.redis import RedisBroker
from prometheus_client import Counter

redis_broker = RedisBroker(host="localhost")
dramatiq.set_broker(redis_broker)

DICE_COUNTER = Counter(
    "worker_dice_rolls_total",
    "Total number of dice rolls labelled per face",
    labelnames=["face"],
)


@dramatiq.actor()
def roll_dice_task():
    result = random.randint(1, 6)
    time.sleep(2)
    DICE_COUNTER.labels(result).inc()
    print(result)


if __name__ == "__main__":
    roll_dice_task.send()
