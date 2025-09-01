# -*- coding: utf-8 -*-
from src.config import get_options


EXPECTED = {
    "department": "数字传媒学院",
    "age_bins": [[0, 30], [31, 50], [51, 80]],
    "majors": ["数字媒体技术", "动画", "网络与新媒体"],
    "title_categories": ["无", "助教", "讲师", "副教授", "教授", "其他高级"],
    "project_statuses": ["申报", "立项", "延期", "结题"],
}


def test_get_options():
    assert get_options("department") == EXPECTED["department"]

    assert get_options("age_bins") == EXPECTED["age_bins"]

    assert get_options("majors") == EXPECTED["majors"]