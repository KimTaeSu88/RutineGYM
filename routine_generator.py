from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class RoutineDay:
    day: int
    focus: str
    exercises: list[str]


_GOAL_TEMPLATES = {
    "근력": ["스쿼트", "벤치프레스", "데드리프트", "오버헤드프레스", "풀업", "런지"],
    "다이어트": ["버피", "점핑잭", "마운틴클라이머", "로잉", "런닝", "스텝업"],
    "유지": ["푸시업", "스쿼트", "플랭크", "걷기", "밴드로우", "스트레칭"],
}

_FOCUS_SEQUENCE = ["상체", "하체", "코어", "전신", "유산소"]


def generate_workout_routine(goal: str = "유지", days_per_week: int = 3) -> list[RoutineDay]:
    if goal not in _GOAL_TEMPLATES:
        raise ValueError(f"지원하지 않는 목표입니다: {goal}")
    if not 1 <= days_per_week <= 7:
        raise ValueError("운동 일수는 1~7 사이여야 합니다.")

    template = _GOAL_TEMPLATES[goal]
    routine: list[RoutineDay] = []
    for day in range(1, days_per_week + 1):
        start = (day - 1) % len(template)
        exercises = [template[(start + offset) % len(template)] for offset in range(3)]
        routine.append(
            RoutineDay(
                day=day,
                focus=_FOCUS_SEQUENCE[(day - 1) % len(_FOCUS_SEQUENCE)],
                exercises=exercises,
            )
        )
    return routine


def format_routine(routine: list[RoutineDay]) -> str:
    lines: list[str] = []
    for day in routine:
        lines.append(f"Day {day.day} ({day.focus}): {', '.join(day.exercises)}")
    return "\n".join(lines)


if __name__ == "__main__":
    routine = generate_workout_routine()
    print(format_routine(routine))
