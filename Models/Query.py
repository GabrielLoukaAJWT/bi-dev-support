from dataclasses import dataclass, field
import datetime
from typing import Optional


@dataclass
class Query:
    initTime: datetime = datetime.datetime(1, 1, 1, 0, 0)
    endTime: datetime = datetime.datetime(1, 1, 1, 0, 0)
    execTime: datetime.timedelta = datetime.timedelta()
    columns: list = field(default_factory=lambda: [])
    rows: list = field(default_factory=lambda: [])


@dataclass
class QueryLog:
    id: int
    query: Query