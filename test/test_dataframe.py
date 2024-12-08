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
    new_df = df[Series([True, False, True])]
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


TEST_DATA = {
    "SKU": Series(["A001", "A002", "A003", None]),
    "price": Series([12.5, 7.0, 5.0, None]),
    "sales": Series([5, 3, 8, None]),
    "taxed": Series([True, False, True, None]),
}


def test_None_type_operations():
    df = DataFrame(TEST_DATA)

    assert df["SKU"] == Series(["A001", "A002", "A003", None])


def test_price():
    df = DataFrame(TEST_DATA)

    df_price_one = df["price"] + 5.0
    assert df_price_one == Series([17.5, 12.0, 10.0, None])

    df_price_filter = df_price_one > 10.0
    assert df_price_filter == Series([True, True, False, False])

    assert df[df_price_filter]["SKU"] == Series(["A001", "A002"])


def test_sales():
    df = DataFrame(TEST_DATA)

    df_sales_filter = df["sales"] > 3
    assert df_sales_filter == Series([True, False, True, False])
    assert df[df_sales_filter]["SKU"] == Series(["A001", "A003"])


def test_price_and_sales():
    df = DataFrame(TEST_DATA)

    df_price_one = df["price"] + 5.0
    df_price_filter = df_price_one > 10.0
    df_sales_filter = df["sales"] > 3

    df_price_and_sales = df_price_filter & df_sales_filter
    assert df_price_and_sales == Series([True, False, False, False])


def test_not_taxed():
    df = DataFrame(TEST_DATA)

    df_not_taxed = ~df["taxed"]
    assert df_not_taxed == Series([False, True, False, None])

    print(df_not_taxed)
    df_not_taxed_filter = df[df_not_taxed]["SKU"]
    assert df_not_taxed_filter == Series(["A002"])


TEST_DATA = {
    "SKU": Series(["X4E", "T3B", "F8D", "C7X"]),
    "price": Series([7.0, 3.5, 8.0, 6.0]),
    "sales": Series([5, 3, 1, 10]),
    "taxed": Series([False, False, True, False]),
}


def test_official():
    df = DataFrame(TEST_DATA)
    print(df)

    result = df[(df["price"] + 5.0 > 10.0) & (df["sales"] > 3) & ~df["taxed"]]["SKU"]
    print(result)

    # let's find all our tax free products/SKUs where the price + our $5.0 shipping fee is more than $10 and we had more than 3 sales

    # expected result:
    # tax free -> no F8D, price + 5 >10 means no T3B,
    # both X4E and C7X have more than 3 sales
    expected_result = Series(["X4E", "C7X"])
    assert result == expected_result


def test_price():
    df = DataFrame(TEST_DATA)

    df_price_one = df["price"] + 5.0
    assert df_price_one == Series([12.0, 8.5, 13.0, 11.0])

    df_price_filter = df_price_one > 10.0
    assert df_price_filter == Series([True, False, True, True])

    assert df[df_price_filter]["SKU"] == Series(["X4E", "F8D", "C7X"])


def test_sales():
    df = DataFrame(TEST_DATA)

    df_sales_filter = df["sales"] > 3
    assert df_sales_filter == Series([True, False, False, True])
    assert df[df_sales_filter]["SKU"] == Series(["X4E", "C7X"])


def test_price_and_sales():
    df = DataFrame(TEST_DATA)

    df_price_one = df["price"] + 5.0
    df_price_filter = df_price_one > 10.0
    df_sales_filter = df["sales"] > 3

    df_price_and_sales = df_price_filter & df_sales_filter
    assert df_price_and_sales == Series([True, False, False, True])


def test_not_taxed():
    df = DataFrame(TEST_DATA)

    df_not_taxed = ~df["taxed"]
    assert df_not_taxed == Series([True, True, False, True])
    df_not_taxed_filter = df[df_not_taxed]["SKU"]
    assert df_not_taxed_filter == Series(["X4E", "T3B", "C7X"])
