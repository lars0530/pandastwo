from typing import Self, Type


class Series[LT]:  # LT is a Generic Type for list type
    """stores data in a one-dimensional array"""

    def __init__(self, data: list[LT]) -> None:
        if not data:
            raise ValueError("data cannot be empty")
        if len(data) == 0:  # NOT SURE ABOUT THIS
            raise ValueError("data cannot be empty")

        data_type = self._find_data_type(data)
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
        if isinstance(index, int):
            if index < 0 or index >= len(self.data):
                raise IndexError("index out of range")
            return self.data[index]

        elif isinstance(index, list):
            # test index length == data_length
            if len(index) != len(self.data):
                raise ValueError("index must have the same length as the data")
            return Series([self.data[i] for i in range(len(index)) if index[i]])
        else:
            raise ValueError("index must be an integer or a list of booleans")

    def __len__(self) -> int:
        return len(self.data)
