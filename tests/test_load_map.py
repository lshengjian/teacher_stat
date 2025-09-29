import include

from src.utils import load_define


def test_load_define():
    data = load_define("teacher")
    assert data[0]['name_en'] == 'employee_id'
    assert data[0]['name_zh'] == '工号'
    assert data[0]['type'] == 'String(5)'
    assert data[-2]['name_en'] == '@age'
    assert data[-2]['name_zh'] == '年龄'
    assert data[-2]['type'] == 'Integer'