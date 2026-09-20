from __future__ import annotations

from datetime import date, timedelta


def review(ease: float, interval: int, repetitions: int, quality: int) -> tuple[float, int, int]:
    """SM-2. quality: again=1, hard=3, good=4, easy=5."""
    quality = max(0, min(5, quality))
    if quality < 3:
        return max(1.3, ease), 1, 0

    if repetitions == 0:
        new_interval = 1
    elif repetitions == 1:
        new_interval = 3 if quality == 3 else 6
    else:
        factor = ease if quality >= 4 else max(1.3, ease - 0.15)
        new_interval = max(1, round(interval * factor))
        if quality == 3:
            new_interval = max(1, round(new_interval * 0.7))

    new_ease = ease + (0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02))
    new_ease = max(1.3, min(2.8, new_ease))
    return new_ease, new_interval, repetitions + 1


def due_on(interval_days: int, today: date | None = None) -> str:
    day = today or date.today()
    return (day + timedelta(days=interval_days)).isoformat()
