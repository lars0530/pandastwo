from pandastwo.dataframe import DataFrame
from pandastwo.series import Series


def test_test():
    assert True


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

    # assert df[df_price_filter]["SKU"] == Series(["X4E", "F8D", "C7X"])


def test_sales():
    df = DataFrame(TEST_DATA)

    df_sales_filter = df["sales"] > 3
    assert df_sales_filter == Series([True, False, False, True])
    # assert df[df_sales_filter]["SKU"] == Series(["X4E", "C7X"])


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
