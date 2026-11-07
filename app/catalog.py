"""Pure unit-validation rule for BuildMart product measurements."""

SUPPORTED_UNITS = frozenset({"шт.", "кг", "т", "м³", "мешок"})


def is_valid_unit(unit: str | None) -> bool:
    return unit in SUPPORTED_UNITS
