# -*- coding: utf-8 -*-

from src.merge_files import merge_teacher_files



def test_get_options():
    fname,all_base, all_projects = merge_teacher_files()
    assert fname == "数字传媒学院.xlsx"
    assert not all_base.empty
    assert not all_projects.empty