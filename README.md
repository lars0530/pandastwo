# pandastwo

pandastwo is a prototype library designed to address some of the limitations of pandas, specifically in handling null values and type consistency. This project is a small Python programming exercise to demonstrate these improvements.

## Features

- **DataFrame and Series**: Supports DataFrames and Series
    - DataFrames consist of multiple Series of the same length
- **Strict Type Handling**: Each Series in a DataFrame holds values of a specific type, with explicit handling for `None`.
    - Supported types are: `int`, `float`, `bool` and `str`
- **Null Value Support**: Differentiates between `None` and `NaN` values.
    - `None` values are tolerated and propagate through operations, while `NaN` values cause errors
- **Element-wise Operations**: Supports element-wise operations for numeric and boolean Series
    - Mathematical operations (`+,-,*,/`) for all numeric types
    - Equailty operation (`==`) for all types
    - Inequality (`!=, >, <, <=, >=`) operations for number types
    - `and`, `or`, ``xor`` and ``invert`` operations for boolean types


## Usage

### Creating a DataFrame

```python
from pandastwo import DataFrame, Series

data = {
    "SKU": Series(["X4E", "T3B", "F8D", "C7X"]),
    "price": Series([7.0, 3.5, 8.0, 6.0]),
    "sales": Series([5, 3, 1, 10]),
    "taxed": Series([False, False, True, False]),
}

df = DataFrame(data)
```

### Querying Data

```python
result = df[(df["price"] + 5.0 > 10.0) & (df["sales"] > 3) & ~df["taxed"]]["SKU"]
print(result)

# Series(["X4E", "C7X"])
```

## Getting Started (for developers)
Prerequisites: 
- uv ([Download](https://docs.astral.sh/uv/getting-started/installation/))

```bash
# clone repo
git clone https://github.com/yourusername/pandastwo.git
cd pandastwo

# create new virtual environment
uv venv

# install dependencies
uv sync --dev

# run tests
uv run pytest
```