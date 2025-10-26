import sys
from collections import Counter
from typing import Dict, List, Optional


def parse_log_line(line: str) -> Dict[str, str]:
    """
    Парсить рядок логу формату:
    YYYY-MM-DD HH:MM:SS LEVEL Message...
    Повертає dict із ключами: date, time, level, message.
    """
    parts = line.strip().split(maxsplit=3)
    if len(parts) < 4:
        raise ValueError("Неправильний формат рядка логу")
    date, time, level, message = parts[0], parts[1], parts[2], parts[3]
    return {"date": date, "time": time, "level": level, "message": message}


def load_logs(file_path: str) -> List[Dict[str, str]]:
    """
    Зчитує лог-файл і повертає список словників (розібраних рядків).
    """
    logs: List[Dict[str, str]] = []
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            try:
                logs.append(parse_log_line(line))
            except ValueError:
                # Пропускаємо некоректні рядки, але можна логувати у stderr
                continue
    return logs


def filter_logs_by_level(logs: List[Dict[str, str]], level: str) -> List[Dict[str, str]]:
    """
    Повертає всі записи конкретного рівня (рівні регістронезалежні).
    """
    level_up = level.upper()
    return [rec for rec in logs if rec["level"].upper() == level_up]


def count_logs_by_level(logs: List[Dict[str, str]]) -> Dict[str, int]:
    """
    Рахує кількість записів за рівнем логування.
    """
    counts = Counter(rec["level"].upper() for rec in logs)
    # Гарантуємо наявність ключів для 4 рівнів із умови
    for k in ("INFO", "DEBUG", "ERROR", "WARNING"):
        counts.setdefault(k, 0)
    return dict(counts)


def display_log_counts(counts: Dict[str, int]) -> None:
    """
    Виводить таблицю "Рівень логування | Кількість".
    """
    print("Рівень логування | Кількість")
    print("-----------------|----------")
    for level in ("INFO", "DEBUG", "ERROR", "WARNING"):
        print(f"{level:<16} | {counts.get(level, 0)}")


def main(argv: Optional[List[str]] = None) -> int:
    """
    Використання:
      python main.py path/to/logfile.log
      python main.py path/to/logfile.log error
    """
    argv = argv if argv is not None else sys.argv[1:]
    if not argv:
        print("Вкажіть шлях до лог-файлу. Приклад: python main.py sample.log")
        return 2

    file_path = argv[0]
    wanted_level = argv[1] if len(argv) > 1 else None

    try:
        logs = load_logs(file_path)
    except FileNotFoundError:
        print(f"Файл не знайдено: {file_path}")
        return 2
    except UnicodeDecodeError:
        print(f"Помилка кодування при читанні: {file_path}")
        return 2

    counts = count_logs_by_level(logs)
    display_log_counts(counts)

    if wanted_level:
        lvl = wanted_level.upper()
        selected = filter_logs_by_level(logs, lvl)
        print(f"\nДеталі логів для рівня '{lvl}':")
        for rec in selected:
            print(f"{rec['date']} {rec['time']} - {rec['message']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
