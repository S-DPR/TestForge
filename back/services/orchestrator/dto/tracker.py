from dataclasses import dataclass
from typing import Optional


@dataclass
class TrackerData:
    filename: str
    diff_status: str
    code1_status: str
    code2_status: str
    error_status: Optional[Exception] = None
