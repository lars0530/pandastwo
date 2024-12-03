from typing import Self, Type


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

    def __getitem__(
        self, index: int | list[bool]
    ) -> LT | Self:  # should be LT | Series
        if not isinstance(index, int) and not isinstance(index, list):
            raise ValueError("index must be an integer or a list of booleans")

        if isinstance(index, int):
            if index < 0 or index >= len(self.data):
                raise IndexError("index out of range")
            return self.data[index]

        if isinstance(index, list):
            # test index length == data_length
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

    def __add__(self, other: Self) -> Self:
        if isinstance(other, int) or isinstance(other, float):
            # if other is a scalar, make it a Series and continue add operation
            other = Series([other for _ in self.data])

        if not isinstance(other, Series):
            raise ValueError("Only Series can be added to another Series")

        if len(self) != len(other):
            raise ValueError("Series must have the same length")

        # check if both data types are numeric
        if self.data_type not in [int, float] or other.data_type not in [int, float]:
            raise ValueError("Series must have numeric data types to be added")

        # cast to float if any of the data types is float
        if self.data_type == float or other.data_type == float:
            data = []
            for x, y in zip(self.data, other.data):
                if x is None or y is None:
                    data.append(None)
                else:
                    data.append(float(x) + float(y))
            return Series(data)

        else:  # return int Series
            data = []
            for x, y in zip(self.data, other.data):
                if x is None or y is None:
                    data.append(None)
                else:
                    data.append(x + y)
            return Series(data)

    def __sub__(self, other: Self) -> Self:
        if isinstance(other, int) or isinstance(other, float):
            # if other is a scalar, make it a Series and continue add operation
            other = Series([other for _ in self.data])

        if not isinstance(other, Series):
            raise ValueError("Only Series can be added to another Series")

        if len(self) != len(other):
            raise ValueError("Series must have the same length")

        # check if both data types are numeric
        if self.data_type not in [int, float] or other.data_type not in [int, float]:
            raise ValueError("Series must have numeric data types to be added")

        # cast to float if any of the data types is float
        if self.data_type == float or other.data_type == float:
            data = []
            for x, y in zip(self.data, other.data):
                if x is None or y is None:
                    data.append(None)
                else:
                    data.append(float(x) - float(y))
            return Series(data)

        else:  # return int Series
            data = []
            for x, y in zip(self.data, other.data):
                if x is None or y is None:
                    data.append(None)
                else:
                    data.append(x - y)
            return Series(data)
