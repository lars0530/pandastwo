from typing import Self, overload
from pandastwo.series import Series


class DataFrame:
    def __init__(self, data: dict[str, Series]) -> None:
        # currently data cannot be empty because there is no way to add data and an empty Series is not useful
        # this should be changed in the future when adding data is implemented
        if not data:
            raise ValueError("data cannot be empty")
        if not isinstance(data, dict):
            raise ValueError(f"data must be of type dictionary (found: {type(data)})")
        # check all keys are string, all values are Series
        for key, value in data.items():
            if not isinstance(key, str):
                raise ValueError(
                    f"all dataframe keys must be strings (found: {type(key)})"
                )
            if not isinstance(value, Series):
                raise ValueError(
                    f"all dataframe values must be Series (found: {type(value)})"
                )
        # check all Series have same length
        self._check_series_lengths(data)

        self.data = data

    def _check_series_lengths(self, data: dict[str, Series]) -> None:
        lengths = {key: len(series) for key, series in data.items()}
        if len(set(lengths.values())) > 1:
            raise ValueError(f"all Series must have the same length (found: {lengths})")

    @overload
    def __getitem__(self, index: str) -> Series: ...
    @overload
    def __getitem__(self, index: Series) -> Self: ...

    def __getitem__(self, key: str | Series) -> Series | Self:
        if not isinstance(key, str) and not isinstance(
            key, Series
        ):  # ideally check if not isinstance(key, Series[bool])
            raise ValueError(
                f"a dataframe key must be a string or a Series of booleans (found: {type(key)})"
            )

        if isinstance(key, str):
            if key not in self.data.keys():
                raise KeyError(f"key {key} not found in dataframe")
            return self.data[key]

        if isinstance(
            key, Series
        ):  # ideally check if not isinstance(key, Series[bool]), but this is not possible
            if len(key) != len(next(iter(self.data.values()))):
                raise ValueError(
                    f"Boolean Series key must have the same length as the data (key length: {len(key)}, data length: {len(list(self.data.values())[0])})"
                )
            for k in key.data:
                if k is not None and not isinstance(
                    k, bool
                ):  # if k is neither None nor bool -> unallowed type
                    raise ValueError(
                        f"Boolean Series key must contain only booleans or None type (found: {type(k)})"
                    )
            return DataFrame({k: self.data[k][key] for k in self.data.keys()})

    def __repr__(self):
        return str(self.data)
