import re
from typing import Callable, Generator


def generator_numbers(text: str) -> Generator[float, None, None]:
    """
    Ітерує всі дійсні числа, які у тексті чітко відокремлені ПРОБІЛАМИ з обох боків.
    Порада з умови: числа «записані без помилок».
    """
    # Додаємо по пробілу з країв, щоб знайти число на початку/в кінці рядка
    padded = f" {text} "
    pattern = r"(?<=\s)\d+(?:\.\d+)?(?=\s)"
    for m in re.finditer(pattern, padded):
        yield float(m.group())


def sum_profit(text: str, func: Callable[[str], Generator[float, None, None]]) -> float:
    """
    Повертає суму чисел, які повертає генератор func(text).
    """
    return round(sum(func(text)), 2)


if __name__ == "__main__":
    text = ("Загальний дохід працівника складається з декількох частин: "
            "1000.01 як основний дохід, доповнений додатковими надходженнями "
            "27.45 і 324.00 доларів.")
    total = sum_profit(text, generator_numbers)
    print(f"Загальний дохід: {total}")  # 1351.46
