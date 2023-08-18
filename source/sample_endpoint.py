""" 
Created on : 18/08/23 12:42 pm
@author : ds  
"""

def my_function(a_num, b_num):
    """
    This is to test Pytest and pytest coverage
    :param a_num:  an integer
    :param b_num: an integer
    :return: string
    """
    if a_num > b_num:
        return f"{a_num} is greater than {b_num}"
    elif a_num < b_num:
        return f"{a_num} is smaller than {b_num}"

    return f"{a_num} and {b_num} are equal"

