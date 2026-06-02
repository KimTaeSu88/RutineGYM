from __future__ import annotations

import random

from .catalog import EXERCISES
from .models import Difficulty, Routine, RoutineItem, Target


def rest_seconds_for(difficulty: Difficulty) -> int:
    return {
        Difficulty.BEGINNER: 60,
        Difficulty.INTERMEDIATE: 45,
        Difficulty.ADVANCED: 30,
    }[difficulty]


def set_count_for(minutes: int, difficulty: Difficulty) -> int:
    # 간단한 MVP 규칙: 시간 기반으로 대략적인 세트 수를 고정.
    # (향후 실제 총 소요시간 추정 기반으로 보정 가능)
    if minutes <= 10:
        return 3 if difficulty != Difficulty.ADVANCED else 4
    if minutes <= 20:
        return 4
    return 4 if difficulty == Difficulty.BEGINNER else 5


def items_per_set_for(minutes: int) -> int:
    if minutes <= 10:
        return 3
    if minutes <= 20:
        return 4
    return 5


def _difficulty_rank(d: Difficulty) -> int:
    return {Difficulty.BEGINNER: 1, Difficulty.INTERMEDIATE: 2, Difficulty.ADVANCED: 3}[d]


def _eligible(minutes: int, difficulty: Difficulty, target: Target, quiet_mode: bool, has_pushup_board: bool) -> list:
    max_noise = "medium" if quiet_mode else "loud"
    allowed_noise = {"quiet"} | ({"medium"} if max_noise in {"medium", "loud"} else set()) | (
        {"loud"} if max_noise == "loud" else set()
    )

    rank = _difficulty_rank(difficulty)

    eligible = []
    for ex in EXERCISES:
        if _difficulty_rank(ex.min_difficulty) > rank:
            continue
        if ex.noise_level not in allowed_noise:
            continue
        if target not in ex.targets and target != Target.FULL_CORE:
            # 타겟이 '전체 코어'가 아니면 해당 타겟 포함 동작을 우선
            continue
        if minutes < 30 and ex.id in {"push_up"}:
            # 상체/보드 활용은 30분에서만 기본 채택(요구사항 반영)
            continue
        if minutes >= 30 and ex.id == "push_up" and not has_pushup_board:
            # 보드가 없더라도 푸시업 자체는 가능하므로 제외하지 않음.
            pass
        eligible.append(ex)

    # 전체 코어 타겟은 다양성 우선: 모든 코어 동작을 대상에 포함
    if target == Target.FULL_CORE:
        eligible = [ex for ex in EXERCISES if _difficulty_rank(ex.min_difficulty) <= rank and ex.noise_level in allowed_noise]
        if minutes < 30:
            eligible = [ex for ex in eligible if ex.id != "push_up"]

    return eligible


def _amount_for(ex_id: str, difficulty: Difficulty, minutes: int) -> int:
    # 아주 단순한 볼륨 테이블(MVP). 실제로는 세트 수/총 시간 기반으로 조정 가능.
    if ex_id in {"plank", "side_plank"}:
        base = 20 if difficulty == Difficulty.BEGINNER else 30 if difficulty == Difficulty.INTERMEDIATE else 40
        if minutes >= 30:
            base += 10
        return base
    if ex_id in {"flutter_kick", "mountain_climber_low_impact"}:
        base = 20 if difficulty == Difficulty.BEGINNER else 30 if difficulty == Difficulty.INTERMEDIATE else 40
        return base

    # reps
    base = 10 if difficulty == Difficulty.BEGINNER else 14 if difficulty == Difficulty.INTERMEDIATE else 18
    if minutes >= 20:
        base += 2
    return base


def generate_routine(
    *,
    difficulty: Difficulty,
    minutes: int,
    target: Target,
    quiet_mode: bool = True,
    has_pushup_board: bool = False,
    seed: int | None = None,
) -> Routine:
    rng = random.Random(seed)

    eligible = _eligible(minutes, difficulty, target, quiet_mode, has_pushup_board)
    if not eligible:
        raise ValueError("조건에 맞는 동작이 없습니다. 난이도/조용한 모드/타겟을 조정해 주세요.")

    k = items_per_set_for(minutes)
    rng.shuffle(eligible)
    picked = eligible[:k] if len(eligible) >= k else (eligible * ((k // len(eligible)) + 1))[:k]

    items = [RoutineItem(exercise=ex, amount=_amount_for(ex.id, difficulty, minutes)) for ex in picked]

    title = f"{difficulty.value} · {minutes}분 · {target.value}"
    return Routine(
        title=title,
        difficulty=difficulty,
        minutes=minutes,
        target=target,
        set_count=set_count_for(minutes, difficulty),
        rest_seconds=rest_seconds_for(difficulty),
        items=items,
    )

