from typing import Self, overload
from pandastwo.series import Series


class DataFrame:
    """
    A class representing a DataFrame-like structure with labeled columns.

    Attributes
    ----------
    data : dict[str, Series]
        A dictionary where keys are column names and values are Series objects.
    """

    def __init__(self, data: dict[str, Series]) -> None:
        """
        Initialize the DataFrame with the provided data.

        Parameters
        ----------
        data : dict[str, Series]
            A dictionary where keys are strings representing column names
            and values are Series objects.

        Raises
        ------
        ValueError
            If data is empty, not a dictionary, or contains invalid keys or values.
        """
        if not data:
            raise ValueError("data cannot be empty")
        if not isinstance(data, dict):
            raise ValueError(f"data must be of type dictionary (found: {type(data)})")
        for key, value in data.items():
            if not isinstance(key, str):
                raise ValueError(
                    f"all dataframe keys must be strings (found: {type(key)})"
                )
            if not isinstance(value, Series):
                raise ValueError(
                    f"all dataframe values must be Series (found: {type(value)})"
                )
        self._check_series_lengths(data)

        self.data = data

    def _check_series_lengths(self, data: dict[str, Series]) -> None:
        """
        Validate that all Series objects in the data have the same length.

        Parameters
        ----------
        data : dict[str, Series]
            A dictionary of column names and Series objects.

        Raises
        ------
        ValueError
            If Series objects have differing lengths.
        """
        lengths = {key: len(series) for key, series in data.items()}
        if len(set(lengths.values())) > 1:
            raise ValueError(f"all Series must have the same length (found: {lengths})")

    @overload
    def __getitem__(self, index: str) -> Series: ...

    @overload
    def __getitem__(self, index: Series) -> Self: ...

    def __getitem__(self, index: str | Series) -> Series | Self:
        """
        Retrieve a column by name or filter rows using a boolean Series.

        Parameters
        ----------
        index : str or Series
            The column name as a string or a boolean Series for row filtering.

        Returns
        -------
        Series or DataFrame
            The corresponding column as a Series or a filtered DataFrame.

        Raises
        ------
        ValueError
            If the index is not a string or boolean Series.
        KeyError
            If the column name does not exist.
        ValueError
            If the boolean Series has invalid length or contains non-boolean values.
        """
        if not isinstance(index, str) and not isinstance(index, Series):
            raise ValueError(
                f"a dataframe index must be a string or a Series of booleans (found: {type(index)})"
            )

        if isinstance(index, str):
            if index not in self.data.keys():
                raise KeyError(f"key {index} not found in dataframe")
            return self.data[index]

        if isinstance(index, Series):
            if len(index) != len(next(iter(self.data.values()))):
                raise ValueError(
                    f"Boolean Series index must have the same length as the data (index length: {len(index)}, data length: {len(list(self.data.values())[0])})"
                )
            for k in index.data:
                if k is not None and not isinstance(k, bool):
                    raise ValueError(
                        f"Boolean Series index must contain only booleans or None type (found: {type(k)})"
                    )
            return DataFrame({k: self.data[k][index] for k in self.data.keys()})

    def __repr__(self) -> str:
        """
        Provide a string representation of the DataFrame.

        Returns
        -------
        str
            A formatted string representation of the DataFrame.
        """
        repr_str = "{\n"
        for key, series in self.data.items():
            repr_str += f"  '{key}': {series} (datatype: {series.data_type}),\n"
        repr_str += "}"
        return repr_str
