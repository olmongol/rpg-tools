"""Append-only event log behind a small Store interface.

The PoC target (05) is: JSON-File/SQLite behind a Store interface — *no* Mongo.
LocalJsonStore keeps one append-only ``events.jsonl`` per character under
``<root>/chats/<char>/events.jsonl``. Reads are plain; writes are append +
fsync so a concurrent reader (2nd client) sees a consistent prefix.

Concurrency model: single-writer per character is assumed for the PoC
(a GM approves, a player adds items — both route through the server process).
For the PoC we protect the per-file append with a process-local lock
(os.O_APPEND is atomic on POSIX for the writes we do, but the lock removes any
race in seq numbering across threads in our own tests).
"""

from __future__ import annotations

import json
import os
import threading
from pathlib import Path
from typing import Iterator, List

from .events import Event


_STORE_KEY = b"store"
_store_locks = {}


class Store:
    """Interface shared by the backends (local JSON/SQLite, later Mongo)."""

    def append(self, char: str, event: Event) -> None:  # pragma: no cover - protocol
        raise NotImplementedError

    def read_log(self, char: str) -> List[Event]:  # pragma: no cover - protocol
        raise NotImplementedError

    def last_seq(self, char: str) -> int:  # pragma: no cover - protocol
        """Highest seq in the log, or 0 if empty (so the next seq is 1)."""
        raise NotImplementedError


class LocalJsonStore(Store):
    """One JSONL file per character under ``root/chats/<char>/events.jsonl``."""

    def __init__(self, root: str | os.PathLike) -> None:
        self.root = Path(root)
        self.root.mkdir(parents=True, exist_ok=True)

    def _char_dir(self, char: str) -> Path:
        if not char or char in (".", ".."):
            raise ValueError(f"invalid char name: {char!r}")
        d = self.root / "chats" / char
        d.mkdir(parents=True, exist_ok=True)
        return d

    def _log_path(self, char: str) -> Path:
        return self._char_dir(char) / "events.jsonl"

    def append(self, char: str, event: Event) -> None:
        path = self._log_path(char)
        line = json.dumps(event.to_dict(), ensure_ascii=False,
                          separators=(",", ":")) + "\n"
        lock = self._lock_for(char)
        with lock:
            # Open in binary-append so fsync is well-defined; os.O_APPEND makes
            # the write atomic w.r.t. offset selection on POSIX. The per-char
            # threading.Lock serialises our own process-local writers.
            with open(path, "ab") as fh:
                fh.write(line.encode("utf-8"))
                fh.flush()
                os.fsync(fh.fileno())

    def read_log(self, char: str) -> List[Event] | List[Event]:
        path = self._log_path(char)
        if not path.exists():
            return []
        events: List[Event] = []
        with path.open("r", encoding="utf-8") as fh:
            for i, raw in enumerate(fh, start=1):
                raw = raw.strip()
                if not raw:
                    continue
                try:
                    events.append(Event.from_dict(json.loads(raw)))
                except (json.JSONDecodeError, KeyError, TypeError) as exc:
                    raise ValueError(f"corrupt log line {i} in {path}: {exc}") from exc
        # Defend against accidental seq gaps/dupes from external editors; the
        # canonical order is file order, seq only provides the identifier.
        return events

    def last_seq(self, char: str) -> int:
        last = 0
        path = self._log_path(char)
        if path.exists():
            last_line: str | None = None
            with path.open("r", encoding="utf-8") as fh:
                for raw in fh:
                    raw = raw.strip()
                    if raw:
                        last_line = raw
            if last_line:
                last = max(last, int(json.loads(last_line).get("seq", 0)))
        return last

    def _lock_for(self, char: str) -> threading.Lock:
        lock = _store_locks.get(char)
        if lock is None:
            lock = threading.Lock()
            _store_locks[char] = lock
        return lock
