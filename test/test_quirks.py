import numpy as np

from src.quirks import *
import math
from datetime import datetime
import pytest


@pytest.mark.parametrize("num, output",
                         [('d167ee27-a04b-4c7a-8ac3-e493260ba6a0', 'd167ee27-a04b-4c7a-8ac3-e493260ba6a0'),
                          (1426190831751528152, '1426190831751528152')])
def test_is_valid_donor_id(num, output):
    # # Test Cases:-
    # If UUID is passed.
    # If 19 Digit Number is passed
    assert output == is_valid_donor_id(num)


def test_nan_is_valid_donor_id():
    # Test Case - Passing non UUID and 19 Digit Number
    assert (math.isnan(is_valid_donor_id('asdafadfasfa'))) == True


@pytest.mark.parametrize("num, output", [('	4101', '4101'),
                                         ('(0810)', '0810')])
def test_is_valid_post_code(num, output):
    # Test Case - Finding a 3/4 digit post code
    # Test Case - Find digit having characters other than digits.
    assert is_valid_post_code(num) == output


def test_nan_is_valid_post_code():
    # Test Case - Passing wrong pin codes.
    assert math.isnan(is_valid_post_code('weae af')) == True

    # Test Case - Passing a 5 digit post code
    assert math.isnan(is_valid_post_code('4545232')) == True


def test_nan_is_valid_gender():
    # Test Case 1 - Passing Gender other than F/M.
    assert math.isnan(is_valid_gender('\x0bOther')) == True


@pytest.mark.parametrize("num, output", [('Meal', 'M'),
                                         ('    F', 'F'),
                                         ('M', 'M')])
def test_is_valid_gender(num, output):
    # Test Case - If Geneder value is spelled wrong.
    # Test Case - Gender value is leading by spaces.
    # Test Case - Contains unwanted characters.
    assert is_valid_gender(num) == output


def test_is_valid_birthdate():
    # Test Case 1 - Finding a 3/4 digit post code.
    assert is_valid_birthdate('1974-03-17') == datetime(1974, 3, 17)


def test_nan_is_valid_birthdate():
    # Test Case 2 - Find digit having characters other than digits.
    assert math.isnan(is_valid_birthdate('3541-03-16')) == True


def test_nan_is_valid_donor_type():
    # Test Case 1 - Passing a digit greated than 32 bytes.
    assert math.isnan(is_valid_donor_type(99889983939388391919838391993983728902))\
           == True


@pytest.mark.parametrize("num, output", [(1.0, 1),
                                         ('1.0', 1.0)])
def test_is_valid_donor_type(num, output):
    # Test Case 1 - Find digit having characters other than digits.
    # Test Case 2 - Find digit having characters other than digits.
    assert is_valid_donor_type(num) == output
