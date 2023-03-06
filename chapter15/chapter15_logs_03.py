from loguru import logger


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
