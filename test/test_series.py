from pandastwo.series import StringSeries, BoolSeries, FloatSeries, IntSeries
import pytest

def sanity_check():
    # this is a sanity check to make sure the test is working
    assert 1 == 1
    
def test_series_creation():
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
            
    
            
    
        