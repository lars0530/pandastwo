from pandastwo.dataframe import DataFrame
from pandastwo.series import Series
import pytest


def test_sanity_check():
    # this is a sanity check to make sure the test is working
    assert 1 == 1


def test_dataframe_creation():
    data = {
        "column1": Series([1, 2, 3]),
        "column2": Series([4, 5, 6]),
    }
    df = DataFrame(data)
    assert isinstance(df, DataFrame)
    assert df.data == data


def test_dataframe_creation_with_different_length_series():
    data = {
        "column1": Series([1, 2, 3]),
        "column2": Series([4, 5, 6, 7]),
    }
    with pytest.raises(ValueError):
        DataFrame(data)


def test_dataframe_creation_with_non_string_keys():
    data = {
        1: Series([1, 2, 3]),
        "column2": Series([4, 5, 6]),
    }
    with pytest.raises(ValueError):
        DataFrame(data)


def test_dataframe_creation_with_non_series_values():
    data = {
        "column1": Series([1, 2, 3]),
        "column2": [4, 5, 6],
    }
    with pytest.raises(ValueError):
        DataFrame(data)


def test_dataframe_access_string_key():
    data = {
        "column1": Series([1, 2, 3]),
        "column2": Series([None, 5, 6]),
    }
    df = DataFrame(data)
    assert df["column1"] == Series([1, 2, 3])
    assert df["column2"] == Series([None, 5, 6])


def test_dataframe_access_bool_list():
    data = {
        "column1": Series([1, 2, 3]),
        "column2": Series([None, 5, 6]),
    }
    df = DataFrame(data)
    new_df = df[[True, False, True]]
    assert new_df["column1"] == Series([1, 3])
    assert new_df["column2"] == Series([None, 6])


def test_dataframe_access_bool_list_with_wrong_length():
    data = {
        "column1": Series([1, 2, 3]),
        "column2": Series([None, 5, 6]),
    }
    df = DataFrame(data)
    with pytest.raises(ValueError):
        df[[True, False]]


def test_dataframe_access_non_bool_list():
    data = {
        "column1": Series([1, 2, 3]),
        "column2": Series([None, 5, 6]),
    }
    df = DataFrame(data)
    with pytest.raises(ValueError):
        df[[1, 2, 3]]
