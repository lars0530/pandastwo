from collections.abc import Callable
from typing import Self, Type, overload


class Series[ST]:  # ST is a Generic Type for Series type
    """stores data in a one-dimensional array"""

    def __init__(self, data: list[ST]) -> None:
        # currently data cannot be empty because there is no way to add data and an empty DataFrame is not useful
        # this should be changed in the future when adding data is implemented
        if not data:
            raise ValueError("data cannot be empty")
        if not isinstance(data, list):
            raise ValueError("data must be of type list")

        data_type = self._find_data_type(data)
        self.data_type: type[ST] = data_type
        self._check_data_type_allowed(data_type)
        self._check_data_type(data, data_type)
        self.data: list[ST] = data

    def _find_data_type(self, data: list[ST]) -> Type[ST]:
        for x in data:
            if x is not None:
                return type(x)
        raise ValueError(
            "data cannot be consist of only None types"
        )  # is this a proper assumption? -> for the time being, yes

    def _check_data_type_allowed(self, data_type: Type[ST]) -> None:
        if data_type not in {int, float, bool, str}:
            raise ValueError(
                f"Data type not allowed. (currently: {data_type.__name__}), allowed are: int, float, bool, str"
            )

    def _check_data_type(self, data: list[ST], expected_type: Type[ST]) -> None:
        if not all(isinstance(x, expected_type) or x is None for x in data):
            raise ValueError(
                f"The data must be a of a single type or None. (currently: {expected_type.__name__} or None)"
            )

    @overload
    def __getitem__(self, index: int) -> ST: ...
    @overload
    def __getitem__(self, index: Self) -> Self: ...

    def __getitem__(
        self, index: int | Self
    ) -> ST | Self:  # should be int | Series[bool] -> ST | Series[ST]
        if not isinstance(index, int) and not isinstance(
            index, Series
        ):  # ideally check if isinstance(index, Series[bool])
            raise ValueError("index must be an integer or a Series of booleans")

        if isinstance(index, int):
            if index < 0 or index >= len(self.data):
                raise IndexError("index out of range")
            return self.data[index]

        if isinstance(index, Series):
            if len(index) != len(self.data):
                raise ValueError("index must have the same length as the data")
            for i in index.data:
                if i is not None and not isinstance(
                    i, bool
                ):  # if i is neither None nor bool
                    raise ValueError("Series must contain only booleans or None")
            return Series([self.data[i] for i in range(len(index)) if index[i] is True])

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
        if self.data_type not in {int, float} or other.data_type not in {int, float}:
            raise ValueError("Series must have numeric data types to be operated")

        # cast to float if any of the data types is float
        if self.data_type is float or other.data_type is float or force_float:
            data_float: list[float | None] = []
            for x, y in zip(self.data, other.data):
                if x is None or y is None:
                    data_float.append(None)
                else:
                    data_float.append(operation(float(x), float(y)))
            return Series[float | None](data_float)

        else:  # return int Series
            data_int: list[int | None] = []
            for x, y in zip(self.data, other.data):
                if x is None or y is None:
                    data_int.append(None)
                else:
                    data_int.append(operation(x, y))
            return Series[int | None](data_int)

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
        if self.data_type not in {int, float} or other.data_type not in {int, float}:
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

    def __ne__(self, other: object) -> Self:
        # typing would ideally be __ne__(self, other: Series) -> Series[bool]
        return self._eq_helper_function(other, lambda x, y: x != y)

    def __repr__(self) -> str:
        return f"Series({self.data})"

    def _element_wise_bool_helper_function(
        self, other: Self, operation: Callable
    ) -> Self:
        if not isinstance(other, Series):
            raise ValueError("Only Series can be compared using equality operations")
        if len(self) != len(other):
            raise ValueError("Series must have the same length")
        if self.data_type is not bool or other.data_type is not bool:
            raise ValueError(
                "Series must have the same data type bool, currently: {self.data_type} and {other.data_type}"
            )
        return Series([operation(x, y) for x, y in zip(self.data, other.data)])

    def __and__(self, other: Self) -> Self:
        return self._element_wise_bool_helper_function(other, lambda x, y: x and y)

    def __or__(self, other: Self) -> Self:
        return self._element_wise_bool_helper_function(other, lambda x, y: x or y)

    def __xor__(self, other: Self) -> Self:
        return self._element_wise_bool_helper_function(other, lambda x, y: x ^ y)

    def __invert__(self) -> Self:
        if self.data_type is not bool:
            raise ValueError("Series must have the data type bool to be inverted")
        return Series([not x if x is not None else None for x in self.data])
