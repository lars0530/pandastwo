from abc import ABC
from typing import Sequence, Type


class Series(ABC):
    """stores data in a one-dimensional array"""

    def __init__(self, data: list[str | bool | int | float | None]):
        pass

    def _check_data_type(
        self, data: list[object | None], expected_type: Type[object]
    ) -> None:
        if not all(isinstance(x, expected_type) or x is None for x in data):
            raise ValueError(f"data must be a list of {expected_type.__name__} or None")

    def __getitem__(
        self, index: int | list[bool]
    ) -> str | bool | int | float | None | list[str | bool | int | float | None]:
        if isinstance(index, int):
            if index < 0 or index >= len(self.data):
                raise IndexError("index out of range")
            return self.data[index]

        elif isinstance(index, list):
            # test index length == data_length
            if len(index) != len(self.data):
                raise ValueError("index must have the same length as the data")
            return SeriesFactory([self.data[i] for i in range(len(index)) if index[i]])
        else:
            raise ValueError("index must be an integer or a list of booleans")

    def __len__(self) -> int:
        return len(self.data)


class StringSeries(Series):
    """stores data in a one-dimensional array of strings"""

    def __init__(
        self, data: list[str | None]
    ):  # decide whether to use list or Sequence

        # check types
        self._check_data_type(data, str)

        self.data = data


class BoolSeries(Series):
    """stores data in a one-dimensional array of booleans"""

    def __init__(self, data: list[bool | None]):
        # check types
        self._check_data_type(data, bool)

        self.data = data


class IntSeries(Series):
    """stores data in a one-dimensional array of integers"""

    def __init__(self, data: list[int | None]):
        # check types
        self._check_data_type(data, int)

        self.data = data


class FloatSeries(Series):
    """stores data in a one-dimensional array of floats"""

    def __init__(self, data: list[float | None]):
        # check types
        self._check_data_type(data, float)

        self.data = data


def _find_data_type(data: list[object | None]) -> Type[object] | None:
    for x in data:
        if x is not None:
            return type(x)
    return None


def SeriesFactory(data: list[str | bool | int | float | None]) -> Series:
    # Determine the data type and create the appropriate Series subclass
    # THIS IS VERY HACKY

    data_type = _find_data_type(data)

    # make a guess as to which series is supposed to be created
    if data_type == str:
        return StringSeries(data)
    elif data_type == bool:
        return BoolSeries(data)
    elif data_type == int:
        return IntSeries(data)
    elif data_type == float:
        return FloatSeries(data)
    else:
        raise ValueError(f"Unsupported data type {data_type}")
