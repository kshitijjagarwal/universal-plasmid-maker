from src.ori_finder import ori_finder


def test_find_ori_runs():
    result = ori_finder("examples/pUC19.fa")

    assert isinstance(result, dict)
    assert "ori_positions" in result
    assert isinstance(result["ori_positions"], list)
