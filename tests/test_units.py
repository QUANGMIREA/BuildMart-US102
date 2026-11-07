from app.catalog import is_valid_unit


def test_valid_units():
    assert is_valid_unit("мешок")
    assert is_valid_unit("м³")
    assert is_valid_unit("кг")


def test_invalid_units():
    assert not is_valid_unit("piece")
    assert not is_valid_unit(None)
