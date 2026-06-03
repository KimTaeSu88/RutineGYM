from __future__ import annotations

import json
import os
import sqlite3
from collections.abc import Callable
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, TypeVar

from .models import Routine

T = TypeVar("T")


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def get_db_path() -> Path:
    if os.environ.get("STREAMLIT_RUNTIME_ENV") == "cloud":
        return Path("/tmp/rutinegym.sqlite3")
    return Path("data") / "rutinegym.sqlite3"


def connect(db_path: Path | None = None) -> sqlite3.Connection:
    path = db_path or get_db_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(path.as_posix(), timeout=30)
    conn.row_factory = sqlite3.Row
    return conn


def _with_conn(fn):
    conn = connect()
    try:
        init_db(conn)
        return fn(conn)
    finally:
        conn.close()


def init_db(conn: sqlite3.Connection) -> None:
    conn.executescript(
        """
        CREATE TABLE IF NOT EXISTS routine_history (
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          created_at TEXT NOT NULL,
          title TEXT NOT NULL,
          payload_json TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS favorite_routines (
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          created_at TEXT NOT NULL,
          title TEXT NOT NULL,
          payload_json TEXT NOT NULL
        );
        """
    )
    conn.commit()


def _serialize_routine(routine: Routine) -> str:
    d = asdict(routine)
    # Enum -> value로 정리
    d["difficulty"] = routine.difficulty.value
    d["target"] = routine.target.value
    for item in d["items"]:
        ex = item.get("exercise") or {}
        targets = ex.get("targets") or []
        ex["targets"] = [t.value for t in targets]
        min_diff = ex.get("min_difficulty")
        ex["min_difficulty"] = min_diff.value if hasattr(min_diff, "value") else min_diff
        item["exercise"] = ex
    return json.dumps(d, ensure_ascii=False)


def save_history(routine: Routine) -> int:
    def op(conn: sqlite3.Connection) -> int:
        payload = _serialize_routine(routine)
        cur = conn.execute(
            "INSERT INTO routine_history(created_at, title, payload_json) VALUES (?, ?, ?)",
            (_utc_now_iso(), routine.title, payload),
        )
        conn.commit()
        return int(cur.lastrowid)

    return _with_conn(op)


def save_favorite(routine: Routine) -> int:
    def op(conn: sqlite3.Connection) -> int:
        payload = _serialize_routine(routine)
        cur = conn.execute(
            "INSERT INTO favorite_routines(created_at, title, payload_json) VALUES (?, ?, ?)",
            (_utc_now_iso(), routine.title, payload),
        )
        conn.commit()
        return int(cur.lastrowid)

    return _with_conn(op)


def _rows_to_dicts(rows: list[sqlite3.Row]) -> list[dict[str, Any]]:
    return [dict(row) for row in rows]


def list_history(limit: int = 20) -> list[dict[str, Any]]:
    def op(conn: sqlite3.Connection) -> list[dict[str, Any]]:
        cur = conn.execute(
            "SELECT id, created_at, title FROM routine_history ORDER BY id DESC LIMIT ?",
            (limit,),
        )
        return _rows_to_dicts(cur.fetchall())

    return _with_conn(op)


def list_favorites(limit: int = 50) -> list[dict[str, Any]]:
    def op(conn: sqlite3.Connection) -> list[dict[str, Any]]:
        cur = conn.execute(
            "SELECT id, created_at, title FROM favorite_routines ORDER BY id DESC LIMIT ?",
            (limit,),
        )
        return _rows_to_dicts(cur.fetchall())

    return _with_conn(op)

