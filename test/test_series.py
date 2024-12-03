from pandastwo.series import Series
import pytest


def test_sanity_check():
    # this is a sanity check to make sure the test is working
    assert 1 == 1


def test_sanity_check2():
    x = 1
    assert x == 1


def test_series_creation():
    a = Series(["a", "b", "c"])
    b = Series([True, False, True])
    c = Series([1, 2, 3])
    d = Series([1.0, 2.0, 3.0])
    assert a.data == ["a", "b", "c"]
    assert b.data == [True, False, True]
    assert c.data == [1, 2, 3]
    assert d.data == [1.0, 2.0, 3.0]


def test_series_creation_with_none():
    a = Series(["a", "b", None])
    b = Series([True, False, None])
    c = Series([1, 2, None])
    d = Series([1.0, 2.0, None])
    assert a.data == ["a", "b", None]
    assert b.data == [True, False, None]
    assert c.data == [1, 2, None]
    assert d.data == [1.0, 2.0, None]


def test_type_checking_string():
    with pytest.raises(Exception):
        Series(["1", "2", 3])


def test_type_checking_boolean():
    with pytest.raises(Exception):
        Series([True, 3, False])


def test_type_checking_int():
    with pytest.raises(Exception):
        Series([1, 2, "3"])


def test_type_checking_float():
    with pytest.raises(Exception):
        Series([1.0, 2.0, "3.0"])


# Square brackets operator
def test_square_brackets_index():
    """checks whether square brackets operator returns element at index"""
    a = Series(["a", "b", "c", None])
    assert a[0] == "a"
    assert a[1] == "b"
    assert a[2] == "c"
    assert a[3] == None

    b = Series([True, False, None, True])
    assert b[0] == True
    assert b[1] == False
    assert b[2] == None
    assert b[3] == True

    c = Series([1, 2, 3, None])
    assert c[0] == 1
    assert c[1] == 2
    assert c[2] == 3
    assert c[3] == None

    d = Series([1.0, 2.0, 3.0, None])
    assert d[0] == 1.0
    assert d[1] == 2.0
    assert d[2] == 3.0
    assert d[3] == None


def test_square_brackets_bool_list():
    """checks whether square brackets operator returns elements at True indices as new Series"""
    a = Series(["a", "b", "c", None])
    a_bool_list = a[[True, False, True, False]]
    assert isinstance(a_bool_list, Series)
    assert a_bool_list[0] == "a"
    assert a_bool_list[1] == "c"
    assert len(a_bool_list) == 2
    b = Series([True, False, None, True])

    b_bool_list = b[[False, True, False, True]]
    assert isinstance(b_bool_list, Series)
    assert b_bool_list[0] == False
    assert b_bool_list[1] == True
    assert len(b_bool_list) == 2

    c = Series([1, 2, 3, None])
    c_bool_list = c[[True, False, True, False]]
    assert isinstance(c_bool_list, Series)
    assert c_bool_list[0] == 1
    assert c_bool_list[1] == 3
    assert len(c_bool_list) == 2

    d = Series([1.0, 2.0, 3.0, None])
    d_bool_list = d[[False, True, False, True]]
    assert isinstance(d_bool_list, Series)
    assert d_bool_list[0] == 2.0
    assert d_bool_list[1] == None
    assert len(d_bool_list) == 2


def test_square_brackets_index_out_of_bounds():
    """checks whether square brackets operator raises an exception when index is out of bounds"""
    a = Series(["a", "b", "c", None])
    with pytest.raises(Exception):
        a[4]

    b = Series([True, False, None, True])
    with pytest.raises(Exception):
        b[4]

    c = Series([1, 2, 3, None])
    with pytest.raises(Exception):
        c[4]

    d = Series([1.0, 2.0, 3.0, None])
    with pytest.raises(Exception):
        d[4]


def test_square_brackets_index_wrong_type():
    """checks whether square brackets operator raises an exception when index is not an int"""
    a = Series(["a", "b", "c", None])
    with pytest.raises(Exception):
        a["a"]

    b = Series([True, False, None, True])
    with pytest.raises(Exception):
        b["a"]

    c = Series([1, 2, 3, None])
    with pytest.raises(Exception):
        c["a"]

    d = Series([1.0, 2.0, 3.0, None])
    with pytest.raises(Exception):
        d["a"]


def test_series_creation_with_inferred_type():
    a = Series(["a", "b", "c"])
    assert isinstance(a, Series)

    b = Series([None, False, True])
    assert isinstance(b, Series)

    c = Series([None, None, 3])
    assert isinstance(c, Series)

    d = Series([1.0, None, 3.0])
    assert isinstance(d, Series)


def test_series_creation_empty():
    with pytest.raises(Exception):
        Series()

    with pytest.raises(Exception):
        Series([])

    with pytest.raises(Exception):
        Series([None, None, None])


def test_series_creation_mixed_types():
    with pytest.raises(Exception):
        Series([1, "a", None])

    with pytest.raises(Exception):
        Series([1, 2, 3.0])  # This shall be allowed at some point

    with pytest.raises(Exception):
        Series([1, 2.0, None])  # This as well

    with pytest.raises(Exception):
        Series([1.0, 2, None])  # whis as well

    with pytest.raises(Exception):
        Series([1.0, 2.0, "a"])

    with pytest.raises(Exception):
        Series([True, 2, None])

    with pytest.raises(Exception):
        Series([True, 2.0, None])

    with pytest.raises(Exception):
        Series([True, 2.0, "a"])

    with pytest.raises(Exception):
        Series([True, 2.0, 3])


def test_equality_operation():
    a = Series(["a", "b", "c"])
    b = Series(["a", "b", "c"])
    x = a == b
    assert isinstance(x, Series)
    assert x[0] == True
    assert x[1] == True
    assert x[2] == True

    c = Series([True, False, True])
    d = Series([True, None, True])
    y = c == d
    assert isinstance(y, Series)
    assert y[0] == True
    assert y[1] == False
    assert y[2] == True

    e = Series([3, 2, 3])
    f = Series([1, 2, 3])
    z = e == f
    assert isinstance(z, Series)
    assert z[0] == False
    assert z[1] == True
    assert z[2] == True

    g = Series([None, 2.0, 3.0])
    h = Series([None, 2.0, 3.0])
    w = g == h
    assert isinstance(w, Series)
    assert w[0] == True
    assert w[1] == True
    assert w[2] == True


def test_equality_operation_exceptions():
    a = Series(["a", "b", "c"])
    b = Series(["a"])
    with pytest.raises(Exception):
        a == b

    c = Series([True, False, True])
    d = Series(["a", "b", "c"])
    with pytest.raises(Exception):
        c == d

    e = Series([3, 2, 3])
    f = [1, 2, 3]
    with pytest.raises(Exception):
        e == f


def test_add_operation():
    a = Series([1, 2, 3])
    b = Series([1, 2, 3])
    x = a + b
    assert isinstance(x, Series)
    assert x.data_type == int
    assert x[0] == 2
    assert x[1] == 4
    assert x[2] == 6

    c = Series([1.0, 2.0, 3.0])
    d = Series([1.0, 2.0, 3.0])
    y = c + d
    assert isinstance(y, Series)
    assert y.data_type == float
    assert y[0] == 2.0
    assert y[1] == 4.0
    assert y[2] == 6.0

    e = Series([1, 2, 3])
    f = Series([-1.0, 2.0, 3.0])
    z = e + f
    assert isinstance(z, Series)
    assert z.data_type == float
    assert z[0] == 0.0
    assert z[1] == 4.0
    assert z[2] == 6.0

    g = Series([1, 2, 3])
    h = Series([1, None, 3])
    w = g + h
    assert isinstance(w, Series)
    assert w.data_type == int
    assert w[0] == 2
    assert w[1] == None
    assert w[2] == 6

    i = Series([None, 2.0, 3.0])
    j = Series([1, None, 3])
    l = i + j
    assert isinstance(l, Series)
    assert l.data_type == float
    assert l[0] == None
    assert l[1] == None
    assert l[2] == 6.0


def test_sub_operation():
    a = Series([-10, 20, 30])
    b = Series([1, 2, 3])
    x = a - b
    assert isinstance(x, Series)
    assert x.data_type == int
    assert x[0] == -11
    assert x[1] == 18
    assert x[2] == 27

    c = Series([10.5, 20.5, 30.5])
    d = Series([1.5, -2.5, 3.5])
    y = c - d
    assert isinstance(y, Series)
    assert y.data_type == float
    assert y[0] == 9.0
    assert y[1] == 23.0
    assert y[2] == 27.0

    e = Series([-10, 20, 30])
    f = Series([-1.5, 2.5, 3.5])
    z = e - f
    assert isinstance(z, Series)
    assert z.data_type == float
    assert z[0] == -8.5
    assert z[1] == 17.5
    assert z[2] == 26.5

    g = Series([10, 20, 30])
    h = Series([1, None, -3])
    w = g - h
    assert isinstance(w, Series)
    assert w.data_type == int
    assert w[0] == 9
    assert w[1] == None
    assert w[2] == 33

    i = Series([None, 20.5, 30.5])
    j = Series([10.0, None, 3.5])
    l = i - j
    assert isinstance(l, Series)
    assert l.data_type == float
    assert l[0] == None
    assert l[1] == None
    assert l[2] == 27.0
