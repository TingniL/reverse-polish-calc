import pytest
from app.calculator import evaluate_rpn

def test_simple_add():
    assert evaluate_rpn("2 3 +") == 5

def test_simple_sub():
    assert evaluate_rpn("5 2 -") == 3

def test_simple_mul():
    assert evaluate_rpn("4 3 *") == 12

def test_simple_div():
    assert evaluate_rpn("8 2 /") == 4

def test_invalid_expression():
    with pytest.raises(ValueError):
        evaluate_rpn("2 +")

def test_div_zero():
    with pytest.raises(ZeroDivisionError):
        evaluate_rpn("2 0 /")

def test_complex():
    assert evaluate_rpn("5 1 2 + 4 * + 3 -") == 14 