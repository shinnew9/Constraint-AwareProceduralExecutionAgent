from datetime import datetime


def log(message: str, level: str = "INFO") -> None:
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"[{timestamp}] [{level}] {message}")


def warn(message: str) -> None:
    log(message, level="WARN")


def error(message: str) -> None:
    log(message, level="ERROR")