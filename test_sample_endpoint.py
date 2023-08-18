""" 
Created on : 18/08/23 12:42 pm
@author : ds  
"""

from source.sample_endpoint import my_function


def test_my_function():
    assert "8 is greater than 6" in my_function(8, 6)
    assert "3 is smaller than 7" in my_function(3, 7)
    assert "16 and 16 are equal" in my_function(16, 16)