# %%
from collections.abc import Callable
from typing import Self, Type, overload


class Series[ST]:  # ST is a Generic Type for Series type
    """
    Represents a one-dimensional array of data with support for basic operations and type checking.

    Parameters
    ----------
    data : list[ST]
        The data to store in the series. Must be non-empty and of a single data type.

    Raises
    ------
    ValueError
        If the data is empty or contains unsupported types.
    """

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
        """
        Determines the type of the first non-None element in the data.

        Parameters
        ----------
        data : list[ST]
            The data to analyze.

        Returns
        -------
        Type[ST]
            The type of the first non-None element.

        Raises
        ------
        ValueError
            If all elements are None.
        """
        for x in data:
            if x is not None:
                return type(x)
        raise ValueError("data cannot consist of only None types")

    def _check_data_type_allowed(self, data_type: Type[ST]) -> None:
        """
        Validates that the data type is allowed.

        Parameters
        ----------
        data_type : Type[ST]
            The data type to check.

        Raises
        ------
        ValueError
            If the data type is not in the allowed set.
        """
        if data_type not in {int, float, bool, str}:
            raise ValueError(
                f"Data type not allowed. (currently: {data_type}), allowed are: int, float, bool, str"
            )

    def _check_data_type(self, data: list[ST], expected_type: Type[ST]) -> None:
        """
        Checks that all elements in the data are of the expected type or None.

        Parameters
        ----------
        data : list[ST]
            The data to check.
        expected_type : Type[ST]
            The expected type of the data.

        Raises
        ------
        ValueError
            If any element is not of the expected type or None.
        """
        if not all(isinstance(x, expected_type) or x is None for x in data):
            raise ValueError(
                f"The data must be of a single type or None. (currently: {expected_type} or None)"
            )

    @overload
    def __getitem__(self, index: int) -> ST: ...

    @overload
    def __getitem__(self, index: Self) -> Self: ...

    def __getitem__(self, index: int | Self) -> ST | Self:
        """
        Retrieves elements from the Series based on an integer index or a boolean Series.

        Parameters
        ----------
        index : int or Series
            The index or mask for selecting elements.

        Returns
        -------
        ST or Series[ST]
            The selected element(s).

        Raises
        ------
        ValueError
            If the index is invalid or mismatched in size.
        IndexError
            If the integer index is out of range.
        """
        if not isinstance(index, int) and not isinstance(index, Series):
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
        """
        Returns the number of elements in the Series.

        Returns
        -------
        int
            The length of the Series.
        """
        return len(self.data)

    def __eq__(self, other: object) -> Self:
        """
        Compares the Series for equality with another Series element-wise.

        Parameters
        ----------
        other : object
            The Series to compare against.

        Returns
        -------
        Series[bool]
            A Series of booleans representing equality element-wise.

        Raises
        ------
        ValueError
            If the Series are of different lengths or types.
        """
        if not isinstance(other, Series):
            raise ValueError(
                f"Only Series can be compared using equality operations (found {type(other)})"
            )
        if len(self) != len(other):
            raise ValueError("Series must have the same length")
        if self.data_type != other.data_type:
            raise ValueError("Series must have the same data type")

        return Series([x == y for x, y in zip(self.data, other.data)])

    def _math_helper_function(
        self,
        other: Self,
        operation: Callable,  # Callable[[float, float], float] | Callable[[int, int], int]
        force_float: bool = False,
    ) -> Self:
        """
        Helper function to perform element-wise arithmetic operations.

        Parameters
        ----------
        other : Series or int or float
            The Series or scalar value to operate with.
        operation : Callable
            The arithmetic operation to perform.
        force_float : bool, optional
            Whether to cast results to float, by default False.

        Returns
        -------
        Series
            The result of the operation.

        Raises
        ------
        ValueError
            If the operation is not valid for the data types or lengths.
        """
        if isinstance(other, int) or isinstance(other, float):
            # if other is a scalar, make it a Series and continue operation
            other = Series([other for _ in self.data])
        if not isinstance(other, Series):
            raise ValueError(
                f"Only Series can be operated with another Series (found {type(other)})"
            )
        if len(self) != len(other):
            raise ValueError(
                f"Series must have the same length (found {len(self)} and {len(other)})"
            )
        if self.data_type not in {int, float} or other.data_type not in {int, float}:
            raise ValueError(
                f"Series must have numeric data types to do math operations (found {self.data_type} and {other.data_type})"
            )

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
        """
        Performs element-wise addition with another Series.

        Parameters
        ----------
        other : Series
            The Series to add.

        Returns
        -------
        Series
            The result of the addition.
        """
        return self._math_helper_function(other, lambda x, y: x + y)

    def __sub__(self, other: Self) -> Self:
        """
        Performs element-wise subtraction with another Series.

        Parameters
        ----------
        other : Series
            The Series to subtract.

        Returns
        -------
        Series
            The result of the subtraction.
        """
        return self._math_helper_function(other, lambda x, y: x - y)

    def __mul__(self, other: Self) -> Self:
        """
        Performs element-wise multiplication with another Series.

        Parameters
        ----------
        other : Series
            The Series to multiply.

        Returns
        -------
        Series
            The result of the multiplication.
        """
        return self._math_helper_function(other, lambda x, y: x * y)

    def __truediv__(self, other: Self) -> Self:
        """
        Performs element-wise true division with another Series.

        Parameters
        ----------
        other : Series
            The Series to divide.

        Returns
        -------
        Series
            The result of the division.
        """
        return self._math_helper_function(other, lambda x, y: x / y, force_float=True)

    def _eq_helper_function(self, other: Self, operation: Callable) -> Self:
        """
        Helper function for element-wise comparison operations.

        Parameters
        ----------
        other : Series or int or float
            The Series or scalar to compare with.
        operation : Callable
            The comparison operation to perform.

        Returns
        -------
        Series
            A boolean Series representing the comparison results.

        Raises
        ------
        ValueError
            If the comparison is not valid for the data types or lengths.
        """
        if isinstance(other, int) or isinstance(other, float):
            # if other is a scalar, make it a Series and continue add operation
            other = Series([other for _ in self.data])
        if not isinstance(other, Series):
            raise ValueError(
                f"Only Series can be compared using equality operations (found {type(other)})"
            )
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
        """
        Perform element-wise less-than comparison between two Series.

        Parameters
        ----------
        other : Series
            The Series to compare with.

        Returns
        -------
        Series
            A Series of boolean values representing the comparison results.
        """
        return self._eq_helper_function(other, lambda x, y: x < y)

    def __le__(self, other: Self) -> Self:
        """
        Perform element-wise less-than-or-equal-to comparison between two Series.

        Parameters
        ----------
        other : Series
            The Series to compare with.

        Returns
        -------
        Series
            A Series of boolean values representing the comparison results.
        """
        return self._eq_helper_function(other, lambda x, y: x <= y)

    def __gt__(self, other: Self) -> Self:
        """
        Perform element-wise greater-than comparison between two Series.

        Parameters
        ----------
        other : Series
            The Series to compare with.

        Returns
        -------
        Series
            A Series of boolean values representing the comparison results.
        """
        return self._eq_helper_function(other, lambda x, y: x > y)

    def __ge__(self, other: Self) -> Self:
        """
        Perform element-wise greater-than-or-equal-to comparison between two Series.

        Parameters
        ----------
        other : Series
            The Series to compare with.

        Returns
        -------
        Series
            A Series of boolean values representing the comparison results.
        """
        return self._eq_helper_function(other, lambda x, y: x >= y)

    def __ne__(self, other: object) -> Self:
        """
        Perform element-wise not-equal-to comparison between the Series and another object.

        Parameters
        ----------
        other : object
            The object to compare with. Must be a Series for element-wise comparison.

        Returns
        -------
        Series
            A Series of boolean values representing the comparison results.
        """
        return self._eq_helper_function(other, lambda x, y: x != y)

    def __repr__(self) -> str:
        """
        Return a string representation of the Series.

        Returns
        -------
        str
            A string representation of the Series.
        """
        return f"Series({self.data})"

    def _element_wise_bool_helper_function(
        self, other: Self, operation: Callable
    ) -> Self:
        """
        Perform element-wise boolean operation between two Series.

        Parameters
        ----------
        other : Series
            The Series to perform the operation with.
        operation : Callable
            A function defining the boolean operation to apply.

        Returns
        -------
        Series
            A Series of boolean values resulting from the operation.

        Raises
        ------
        ValueError
            If `other` is not a Series, the lengths differ, or the data types are not boolean.
        """
        if not isinstance(other, Series):
            raise ValueError(
                f"Only Series can be compared using equality operations (found {type(other)})"
            )
        if len(self) != len(other):
            raise ValueError("Series must have the same length")
        if self.data_type is not bool or other.data_type is not bool:
            raise ValueError(
                "Series must have the same data type bool, currently: {self.data_type} and {other.data_type}"
            )
        return Series([operation(x, y) for x, y in zip(self.data, other.data)])

    def __and__(self, other: Self) -> Self:
        """
        Perform element-wise logical AND operation between two Series.

        Parameters
        ----------
        other : Series
            The Series to perform the operation with.

        Returns
        -------
        Series
            A Series of boolean values representing the logical AND results.
        """
        return self._element_wise_bool_helper_function(other, lambda x, y: x and y)

    def __or__(self, other: Self) -> Self:
        """
        Perform element-wise logical OR operation between two Series.

        Parameters
        ----------
        other : Series
            The Series to perform the operation with.

        Returns
        -------
        Series
            A Series of boolean values representing the logical OR results.
        """
        return self._element_wise_bool_helper_function(other, lambda x, y: x or y)

    def __xor__(self, other: Self) -> Self:
        """
        Perform element-wise logical XOR operation between two Series.

        Parameters
        ----------
        other : Series
            The Series to perform the operation with.

        Returns
        -------
        Series
            A Series of boolean values representing the logical XOR results.
        """
        return self._element_wise_bool_helper_function(other, lambda x, y: x ^ y)

    def __invert__(self) -> Self:
        """
        Perform element-wise logical NOT operation on the Series.

        Returns
        -------
        Series
            A Series of boolean values representing the logical NOT results.

        Raises
        ------
        ValueError
            If the Series data type is not boolean.
        """
        if self.data_type is not bool:
            raise ValueError("Series must have the data type bool to be inverted")
        return Series([not x if x is not None else None for x in self.data])
