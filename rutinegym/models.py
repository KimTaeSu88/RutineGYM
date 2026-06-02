from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Literal


class Difficulty(str, Enum):
    BEGINNER = "초급"
    INTERMEDIATE = "중급"
    ADVANCED = "고급"


class Target(str, Enum):
    FULL_CORE = "전체 코어"
    LOWER_ABS = "아랫뱃살"
    OBLIQUES = "옆구리(러브핸들)"


RepType = Literal["reps", "seconds"]


@dataclass(frozen=True)
class Exercise:
    id: str
    name: str
    url: str
    targets: set[Target]
    rep_type: RepType
    noise_level: Literal["quiet", "medium", "loud"]
    min_difficulty: Difficulty
    form_tip: str
    caution: str


@dataclass(frozen=True)
class RoutineItem:
    exercise: Exercise
    amount: int  # reps or seconds


@dataclass(frozen=True)
class Routine:
    title: str
    difficulty: Difficulty
    minutes: int
    target: Target
    set_count: int
    rest_seconds: int
    items: list[RoutineItem]

