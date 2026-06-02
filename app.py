from __future__ import annotations

import streamlit as st

from rutinegym.generator import generate_routine
from rutinegym.models import Difficulty, Target
from rutinegym.storage import connect, init_db, list_favorites, list_history, save_favorite, save_history


st.set_page_config(page_title="RutineGym", page_icon="🛠️", layout="centered")


@st.cache_resource
def _db():
    conn = connect()
    init_db(conn)
    return conn


def _render_routine():
    routine = st.session_state.get("routine")
    if not routine:
        return

    st.subheader(routine.title)
    st.caption(f"세트 수: {routine.set_count} · 세트 간 휴식: {routine.rest_seconds}초")

    for idx, item in enumerate(routine.items, start=1):
        ex = item.exercise
        unit = "초" if ex.rep_type == "seconds" else "회"
        with st.container(border=True):
            st.markdown(f"**{idx}. {ex.name} — {item.amount}{unit}**")
            st.write(f"- 폼: {ex.form_tip}")
            st.write(f"- 주의: {ex.caution}")
            st.link_button("자세 영상/가이드 열기", ex.url)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("히스토리에 저장", use_container_width=True):
            rid = save_history(_db(), routine)
            st.toast(f"저장 완료 (history #{rid})")
    with col2:
        if st.button("즐겨찾기 저장", use_container_width=True):
            rid = save_favorite(_db(), routine)
            st.toast(f"저장 완료 (favorite #{rid})")


def main():
    st.title("나만의 홈트레이닝 코어 빌더")
    st.write("난이도/시간/타겟을 선택하면 오늘의 코어 루틴을 만들어줍니다.")

    with st.sidebar:
        st.subheader("기록")
        if st.button("히스토리 새로고침", use_container_width=True):
            st.rerun()
        st.caption("최근 히스토리")
        for row in list_history(_db(), limit=10):
            st.write(f"- #{row['id']} · {row['created_at']} · {row['title']}")
        st.caption("즐겨찾기")
        for row in list_favorites(_db(), limit=10):
            st.write(f"- #{row['id']} · {row['created_at']} · {row['title']}")

    col_a, col_b, col_c = st.columns(3)

    with col_a:
        difficulty = st.selectbox("1) 난이도", options=list(Difficulty), format_func=lambda d: d.value)
    with col_b:
        minutes = st.selectbox("2) 시간", options=[10, 20, 30], format_func=lambda m: f"{m}분")
    with col_c:
        target = st.selectbox("3) 타겟", options=list(Target), format_func=lambda t: t.value)

    opt1, opt2 = st.columns(2)
    with opt1:
        quiet_mode = st.toggle("조용한 모드(기본 ON)", value=True)
    with opt2:
        has_pushup_board = st.toggle("푸시업 보드 있음", value=False)

    if st.button("루틴 생성", type="primary", use_container_width=True):
        routine = generate_routine(
            difficulty=difficulty,
            minutes=minutes,
            target=target,
            quiet_mode=quiet_mode,
            has_pushup_board=has_pushup_board,
        )
        st.session_state["routine"] = routine

    _render_routine()


if __name__ == "__main__":
    main()

