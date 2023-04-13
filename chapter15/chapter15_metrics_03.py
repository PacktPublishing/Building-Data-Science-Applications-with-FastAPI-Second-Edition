import time

import dramatiq
from dramatiq.brokers.redis import RedisBroker

redis_broker = RedisBroker(host="localhost")
dramatiq.set_broker(redis_broker)


@dramatiq.actor()
def addition_task(a: int, b: int):
    time.sleep(2)
    print(a + b)


if __name__ == "__main__":
    addition_task.send(3, 2)
