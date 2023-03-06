import sys

from loguru import logger

logger.remove()
logger.add(
    sys.stdout,
    level="DEBUG",
    format="<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
    "<level>{level: <8}</level> | "
    "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>"
    " - {extra}",
)


def is_even(n) -> bool:
    logger_context = logger.bind(n=n)
    logger_context.debug("Check if even")
    if not isinstance(n, int):
        logger_context.error("Not an integer")
        raise TypeError()
    return n % 2 == 0


if __name__ == "__main__":
    is_even(2)
    is_even("hello")
