from collections.abc import Callable

ConditionFunction = Callable[[int], bool]


def filter_list(l: list[int], condition: ConditionFunction) -> list[int]:
    return [i for i in l if condition(i)]


def is_even(i: int) -> bool:
    return i % 2 == 0


filter_list([1, 2, 3, 4, 5], is_even)
