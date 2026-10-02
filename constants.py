import pytest

COLOR_CASES = [
    pytest.param(["BLACK"], id="single_black"),
    pytest.param(["GREY"], id="single_grey"),
    pytest.param(["BLACK", "GREY"], id="both_colors"),
    pytest.param([], id="empty_list"),
]

ERROR_LOGIN_ALREADY_USED = "Этот логин уже используется. Попробуйте другой."
ERROR_NOT_ENOUGH_DATA_CREATE = "Недостаточно данных для создания учетной записи"
ERROR_NOT_ENOUGH_DATA_LOGIN = "Недостаточно данных для входа"
ERROR_ACCOUNT_NOT_FOUND = "Учетная запись не найдена"