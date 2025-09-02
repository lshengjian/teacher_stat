import os
from datetime import date, datetime
from typing import  List,  Union, Optional, Iterable
from pathlib import Path
import pandas as pd
ROOT_DIR = Path(__file__).resolve().parents[1]


def ensure_datetime_series(s: pd.Series) -> pd.Series:
    return pd.to_datetime(s, errors="coerce")

def compute_age(birth: Union[pd.Timestamp, datetime, date, str], ref: Optional[date] = None) -> Optional[int]:
    if pd.isna(birth):
        return None
    if isinstance(birth, str):
        try:
            birth = pd.to_datetime(birth, errors="coerce")
        except Exception:
            return None
    if isinstance(birth, pd.Timestamp):
        birth = birth.date()
    if not isinstance(birth, date):
        return None
    ref = ref or date.today()
    years = ref.year - birth.year - ((ref.month, ref.day) < (birth.month, birth.day))
    return int(years)

def label_age_bins(age: Union[int, float, None], bins: List[List[int]]) -> Optional[str]:
    if age is None or pd.isna(age):
        return None
    try:
        age = int(age)
    except Exception:
        return None
    for start, end in bins:
        # 区间为闭区间 [start, end]
        if start <= age <= end:
            return f"{start}-{end}"
    if age<bins[0][0]:
            return  f"<{bins[0][0]}"
    if age>bins[-1][1]:
            return f">{bins[-1][1]}"
    return None

def order_age_categories(bins: List[List[int]]) -> List[str]:
    labels.append(f"<{bins[0][0]}")
    labels = [f"{s}-{e}" for s, e in bins]
    labels.append(f">{bins[-1][1]}")
    return labels


def is_supported_excel(filename: str) -> bool:
    _, ext = os.path.splitext(filename)
    return ext.lower() in  (".xlsx", ".xls") 

def normalize_title(title: str, allowed: Iterable[str]) -> str:
    title = str(title).strip()
    return title if title in allowed else title  # 不强制替换，避免误伤

def try_get_year(s: pd.Series) -> pd.Series:
    s = ensure_datetime_series(s)
    return s.dt.year