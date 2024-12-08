# %%
import sys

sys.path.append("../")  # ONLY for IPython kernel
from typing import Self
from pandastwo.series import Series


class DataFrame:
    def __init__(self, data: dict[str, Series]) -> None:
        # check data is not empty?
        # check all keys are string, all values are Series
        for key, value in data.items():
            if not isinstance(key, str):
                raise ValueError("keys must be strings")
            if not isinstance(value, Series):
                raise ValueError("values must be Series")
        # check all Series have same length
        self._check_series_lengths(data)

        self.data = data

    def _check_series_lengths(self, data: dict[str, Series]) -> None:
        lengths = {key: len(series) for key, series in data.items()}
        if len(set(lengths.values())) > 1:
            raise ValueError("all Series must have the same length")

    def __getitem__(self, key: str | Series) -> "DataFrame":
        if not isinstance(key, str) and not isinstance(
            key, Series
        ):  # ideally check if not isinstance(key, Series[bool])
            raise ValueError("key must be a string or a Series of booleans")

        if isinstance(key, str):
            if not key in self.data.keys():
                raise KeyError(f"key {key} not found")
            return self.data[key]

        if isinstance(
            key, Series
        ):  # ideally check if not isinstance(key, Series[bool])
            for k in key:
                if not isinstance(k, bool):
                    raise ValueError("list must contain only booleans")
            if len(key) != len(next(iter(self.data.values()))):
                raise ValueError("key must have the same length as the data")
            return DataFrame({k: self.data[k][key] for k in self.data.keys()})

    def __repr__(self):
        return str(self.data)


# %%
