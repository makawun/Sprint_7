import pytest

COLOR_CASES = [
    pytest.param(["BLACK"], id="single_black"),
    pytest.param(["GREY"], id="single_grey"),
    pytest.param(["BLACK", "GREY"], id="both_colors"),
    pytest.param([], id="empty_list"),
]