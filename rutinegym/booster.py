from __future__ import annotations

from dataclasses import dataclass
from urllib.parse import quote_plus


@dataclass(frozen=True)
class MusicLink:
    title: str
    url: str
    description: str


def _yt_search(query: str) -> str:
    return f"https://www.youtube.com/results?search_query={quote_plus(query)}"


BOOSTER_BY_MINUTES: dict[int, list[MusicLink]] = {
    10: [
        MusicLink(
            title="10분 짧은 홈트 BGM",
            url=_yt_search("10 minute home workout music"),
            description="짧고 굵게 끝내는 10분 루틴용 템포 있는 BGM",
        ),
        MusicLink(
            title="10분 코어 집중 플레이리스트",
            url=_yt_search("10 minute core workout music playlist"),
            description="코어 운동 리듬에 맞춘 10분 믹스",
        ),
        MusicLink(
            title="10분 모닝 에너지 업",
            url=_yt_search("10 minute morning workout music upbeat"),
            description="기상 후·퇴근 전 가볍게 풀기 좋은 업비트",
        ),
    ],
    20: [
        MusicLink(
            title="20분 홈트 표준 BGM",
            url=_yt_search("20 minute workout music mix"),
            description="20분 표준 루틴에 맞는 중간 템포 믹스",
        ),
        MusicLink(
            title="20분 유산소+코어 플레이리스트",
            url=_yt_search("20 minute cardio core workout music"),
            description="유산소와 코어를 섞은 20분 루틴용",
        ),
        MusicLink(
            title="20분 HIIT 스타일 (저충격)",
            url=_yt_search("20 minute low impact hiit workout music"),
            description="땀 흘리되 층간소음 걱정 줄인 템포",
        ),
    ],
    30: [
        MusicLink(
            title="30분 전신 서킷 BGM",
            url=_yt_search("30 minute full body workout music"),
            description="30분 상체·코어 서킷에 맞는 롱 믹스",
        ),
        MusicLink(
            title="30분 고강도 운동 플레이리스트",
            url=_yt_search("30 minute intense workout music playlist"),
            description="고급 난이도·긴 세션용 고에너지 BGM",
        ),
        MusicLink(
            title="30분 플랭크·코어 집중",
            url=_yt_search("30 minute plank core workout music"),
            description="플랭크·코어 위주 긴 루틴용 스테디 비트",
        ),
    ],
}


def get_booster_links(minutes: int) -> list[MusicLink]:
    return BOOSTER_BY_MINUTES.get(minutes, BOOSTER_BY_MINUTES[20])
