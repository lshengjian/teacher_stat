from __future__ import annotations
from pathlib import Path
import csv



def load_define(name: str) -> list[dict]:
    DEFINES_DIR = Path(__file__).resolve().parents[2] / "defines"

    rt=None

    path = DEFINES_DIR / f'{name}.csv'
    with open(path, mode='r', encoding='utf-8') as csvfile:
        # 创建一个 DictReader 对象
        # 它会自动将第一行作为字典的键
        dict_reader = csv.DictReader(csvfile)
        rt = list(dict_reader)

    

    return rt
