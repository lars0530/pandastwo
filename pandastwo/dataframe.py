from pandastwo.series import Series


class DataFrame:
    def __init__(self, data: dict[str, Series]) -> None:
        # currently data cannot be empty because there is no way to add data and an empty Series is not useful
        # this should be changed in the future when adding data is implemented
        if not data:
            raise ValueError("data cannot be empty")
        if not isinstance(data, dict):
            raise ValueError("data must be of type dictionary")
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
            if key not in self.data.keys():
                raise KeyError(f"key {key} not found")
            return self.data[key]

        if isinstance(
            key, Series
        ):  # ideally check if not isinstance(key, Series[bool]), but this is not possible
            if len(key) != len(next(iter(self.data.values()))):
                raise ValueError(
                    "Boolean Series key must have the same length as the data"
                )
            for k in key.data:
                if k is not None and not isinstance(
                    k, bool
                ):  # if k is neither None nor bool -> unallowed type
                    raise ValueError(
                        "Boolean Series key must contain only booleans or None type"
                    )

            return DataFrame({k: self.data[k][key] for k in self.data.keys()})

    def __repr__(self):
        return str(self.data)
