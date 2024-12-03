from collections.abc import Callable
from typing import Self, Type, overload


class Series[LT]:  # LT is a Generic Type for list type
    """stores data in a one-dimensional array"""

    def __init__(self, data: list[LT]) -> None:
        if not data:
            raise ValueError("data cannot be empty")
        if len(data) == 0:  # NOT SURE ABOUT THIS
            raise ValueError("data cannot be empty")

        data_type = self._find_data_type(data)
        self.data_type: type[LT] = data_type
        self._check_data_type(data, data_type)
        self.data: list[LT] = data

    def _find_data_type(self, data: list[LT]) -> Type[LT]:
        for x in data:
            if x is not None:
                return type(x)
        raise ValueError(
            "data cannot be consist of only None types"
        )  # is this a proper assumption?

    def _check_data_type(self, data: list[LT], expected_type: Type[LT]) -> None:
        if not all(isinstance(x, expected_type) or x is None for x in data):
            raise ValueError(f"data must be a list of {expected_type.__name__} or None")

    @overload
    def __getitem__(self, index: int) -> LT: ...
    @overload
    def __getitem__(self, index: list[bool]) -> Self: ...

    def __getitem__(
        self, index: int | list[bool]
    ) -> LT | Self:  # should be LT | Series
        if not isinstance(index, int) and not isinstance(
            index, list
        ):  # ideally isinstance(index, list[bool])
            raise ValueError("index must be an integer or a list of booleans")

        if isinstance(index, int):
            if index < 0 or index >= len(self.data):
                raise IndexError("index out of range")
            return self.data[index]

        if isinstance(index, list):
            for i in index:
                if not isinstance(i, bool):
                    raise ValueError("list must contain only booleans")
            if len(index) != len(self.data):
                raise ValueError("index must have the same length as the data")
            return Series([self.data[i] for i in range(len(index)) if index[i]])

    def __len__(self) -> int:
        return len(self.data)

    def __eq__(self, other: object) -> Self:
        # should be other: Series -> Series[bool], but mypy doesn't like that
        # fail hard for different lengths
        if not isinstance(other, Series):
            raise ValueError("Only Series can be compared using equality operations")
        if len(self) != len(other):
            raise ValueError("Series must have the same length")
        # fail hard for different types
        if self.data_type != other.data_type:
            raise ValueError("Series must have the same data type")

        # otherwise do element wise returning boolean Series
        return Series(
            [x == y for x, y in zip(self.data, other.data)]
        )  # it wants me to return boolean object

    def _math_helper_function(
        self,
        other: Self,
        operation: Callable,  # Callable[[float, float], float] | Callable[[int, int], int]
        force_float: bool = False,
    ) -> Self:
        if isinstance(other, int) or isinstance(other, float):
            # if other is a scalar, make it a Series and continue operation
            other = Series([other for _ in self.data])
        if not isinstance(other, Series):
            raise ValueError("Only Series can be operated with another Series")
        if len(self) != len(other):
            raise ValueError("Series must have the same length")
        if self.data_type not in [int, float] or other.data_type not in [int, float]:
            raise ValueError("Series must have numeric data types to be operated")

        # cast to float if any of the data types is float
        if self.data_type is float or other.data_type is float or force_float:
            data: list[float | None] = []
            for x, y in zip(self.data, other.data):
                if x is None or y is None:
                    data.append(None)
                else:
                    data.append(operation(float(x), float(y)))
            return Series[float | None](data)

        else:  # return int Series
            data: list[int | None] = []
            for x, y in zip(self.data, other.data):
                if x is None or y is None:
                    data.append(None)
                else:
                    data.append(operation(x, y))
            return Series[int | None](data)

    def __add__(self, other: Self) -> Self:
        return self._math_helper_function(other, lambda x, y: x + y)

    def __sub__(self, other: Self) -> Self:
        return self._math_helper_function(other, lambda x, y: x - y)

    def __mul__(self, other: Self) -> Self:
        return self._math_helper_function(other, lambda x, y: x * y)

    def __truediv__(self, other: Self) -> Self:  # not implementing __floordiv__ for now
        # force_float because 5/3 = 1.666666666.
        return self._math_helper_function(other, lambda x, y: x / y, force_float=True)

    def _eq_helper_function(self, other: Self, operation: Callable) -> Self:
        if isinstance(other, int) or isinstance(other, float):
            # if other is a scalar, make it a Series and continue add operation
            other = Series([other for _ in self.data])
        if not isinstance(other, Series):
            raise ValueError("Only Series can be compared using equality operations")
        if len(self) != len(other):
            raise ValueError("Series must have the same length")
        if self.data_type not in [int, float] or other.data_type not in [int, float]:
            raise ValueError("Series must have numeric data types to be added")
        # check if both data types are numeric
        if self.data_type not in [int, float] or other.data_type not in [int, float]:
            raise ValueError("Series must have numeric data types to be added")

        data: list[bool | None] = []
        for x, y in zip(self.data, other.data):
            if x is None or y is None:
                data.append(None)
            else:
                data.append(operation(x, y))
        return Series[bool | None](data)

    def __lt__(self, other: Self) -> Self:
        return self._eq_helper_function(other, lambda x, y: x < y)

    def __le__(self, other: Self) -> Self:
        return self._eq_helper_function(other, lambda x, y: x <= y)

    def __gt__(self, other: Self) -> Self:
        return self._eq_helper_function(other, lambda x, y: x > y)

    def __ge__(self, other: Self) -> Self:
        return self._eq_helper_function(other, lambda x, y: x >= y)

    def __ne__(self, other: Self) -> Self:
        return self._eq_helper_function(other, lambda x, y: x != y)

    def __repr__(self) -> str:
        return f"Series({self.data})"
