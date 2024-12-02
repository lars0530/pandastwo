from abc import ABC
from typing import Type


class Series(ABC):
    """stores data in a one-dimensional array"""
    
    def __init__(self, data: list[str | bool | int | float | None]):
        # TODO: maybe update type hints, this still allows multiple types
        pass
        
    def _check_data_type(self, data: list[object | None], expected_type: Type[object]) -> None:
        if not all(isinstance(x, expected_type) or x is None for x in data):
            raise ValueError(f"data must be a list of {expected_type.__name__} or None")

        
class StringSeries(Series):
    """stores data in a one-dimensional array of strings"""
    
    def __init__(self, data: list[str|None]):
        
        # check types
        self._check_data_type(data, str)
        
        self.data = data
        
class BoolSeries(Series):
    """stores data in a one-dimensional array of booleans"""
    
    def __init__(self, data: list[bool|None]):
        # check types
        self._check_data_type(data, bool)
        
        self.data = data
        
class IntSeries(Series):
    """stores data in a one-dimensional array of integers"""
    
    def __init__(self, data: list[int|None]):
        # check types
        self._check_data_type(data, int)
        
        self.data = data
        
class FloatSeries(Series):
    """stores data in a one-dimensional array of floats"""
    
    def __init__(self, data: list[float|None]):
        # check types
        self._check_data_type(data, float)
        
        self.data = data