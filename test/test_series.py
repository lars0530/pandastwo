from pandastwo.series import Series, StringSeries, BoolSeries, FloatSeries, IntSeries
import pytest

def sanity_check():
    # this is a sanity check to make sure the test is working
    assert 1 == 1
    
def test_series_creation_with_inferred_type():
    a = StringSeries(["a", "b", "c"])
    b = BoolSeries([True, False, True])
    c = IntSeries([1, 2, 3])
    d = FloatSeries([1.0, 2.0, 3.0])
    assert a.data == ["a", "b", "c"]
    assert b.data == [True, False, True]
    assert c.data == [1, 2, 3]
    assert d.data == [1.0, 2.0, 3.0]
    
def test_series_creation_with_none():
    a = StringSeries(["a", "b", None])
    b = BoolSeries([True, False, None])
    c = IntSeries([1, 2, None])
    d = FloatSeries([1.0, 2.0, None])
    assert a.data == ["a", "b", None]
    assert b.data == [True, False, None]
    assert c.data == [1, 2, None]
    assert d.data == [1.0, 2.0, None]

def test_type_checking_string():
    with pytest.raises(Exception):
        IntSeries(["1", "2", 3])
        
def test_type_checking_boolean():
    with pytest.raises(Exception):
        BoolSeries([True, 3, False])

def test_type_checking_int():
    with pytest.raises(Exception):
        IntSeries([1, 2, "3"])

def test_type_checking_float():
    with pytest.raises(Exception):
        IntSeries([1.0, 2.0, "3.0"])
            
# Square brackets operator
def test_square_brackets_index():
    """checks whether square brackets operator returns element at index"""
    a = StringSeries(["a", "b", "c", None])
    assert a[0] == "a"
    assert a[1] == "b"
    assert a[2] == "c"
    assert a[3] == None
    
    b = BoolSeries([True, False, None, True])
    assert b[0] == True
    assert b[1] == False
    assert b[2] == None
    assert b[3] == True

    c = IntSeries([1, 2, 3, None])
    assert c[0] == 1
    assert c[1] == 2
    assert c[2] == 3
    assert c[3] == None

    d = FloatSeries([1.0, 2.0, 3.0, None])
    assert d[0] == 1.0
    assert d[1] == 2.0
    assert d[2] == 3.0
    assert d[3] == None

def test_square_brackets_bool_list():
    """checks whether square brackets operator returns elements at True indices as new Series"""
    a = StringSeries(["a", "b", "c", None])
    a_bool_list = a[[True, False, True, False]]
    assert isinstance(a_bool_list, StringSeries)
    assert a_bool_list[0] == "a"
    assert a_bool_list[1] == "c"
    assert len(a_bool_list) == 2
    b = BoolSeries([True, False, None, True])
    
    b_bool_list = b[[False, True, False, True]]
    assert isinstance(b_bool_list, BoolSeries)
    assert b_bool_list[0] == False
    assert b_bool_list[1] == True
    assert len(b_bool_list) == 2

    c = IntSeries([1, 2, 3, None])
    c_bool_list = c[[True, False, True, False]]
    assert isinstance(c_bool_list, IntSeries)
    assert c_bool_list[0] == 1
    assert c_bool_list[1] == 3
    assert len(c_bool_list) == 2

    d = FloatSeries([1.0, 2.0, 3.0, None])
    d_bool_list = d[[False, True, False, True]]
    assert isinstance(d_bool_list, FloatSeries)
    assert d_bool_list[0] == 2.0
    assert d_bool_list[1] == None
    assert len(d_bool_list) == 2
    
def test_square_brackets_index_out_of_bounds():
    """checks whether square brackets operator raises an exception when index is out of bounds"""
    a = StringSeries(["a", "b", "c", None])
    with pytest.raises(Exception):
        a[4]
        
    b = BoolSeries([True, False, None, True])
    with pytest.raises(Exception):
        b[4]

    c = IntSeries([1, 2, 3, None])
    with pytest.raises(Exception):
        c[4]

    d = FloatSeries([1.0, 2.0, 3.0, None])
    with pytest.raises(Exception):
        d[4]
        
def test_square_brackets_index_wrong_type():
    """checks whether square brackets operator raises an exception when index is not an int"""
    a = StringSeries(["a", "b", "c", None])
    with pytest.raises(Exception):
        a["a"]
        
    b = BoolSeries([True, False, None, True])
    with pytest.raises(Exception):
        b["a"]

    c = IntSeries([1, 2, 3, None])
    with pytest.raises(Exception):
        c["a"]

    d = FloatSeries([1.0, 2.0, 3.0, None])
    with pytest.raises(Exception):
        d["a"]

def test_series_creation_with_inferred_type():
    a = Series(["a", "b", "c"])
    assert isinstance(a, StringSeries)
    
    b = Series([None, False, True])
    assert isinstance(b, BoolSeries)
    
    c = Series([None, None, 3])
    assert isinstance(c, IntSeries)
    
    d = Series([1.0, None, 3.0])
    assert isinstance(d, FloatSeries)
    
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
        Series([1, 2, 3.0]) # This shall be allowed at some point
        
    with pytest.raises(Exception):
        Series([1, 2.0, None]) # This as well
        
    with pytest.raises(Exception):
        Series([1.0, 2, None]) # whis as well
        
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
    