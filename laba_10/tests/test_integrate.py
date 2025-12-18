import pytest
import math
from integrates import integrate

def test_cos_integral():
    """Проверка интеграла cos(x) на [0, π/2]"""
    result = integrate(math.cos, 0, math.pi/2, n_iter=100000)
    assert abs(result - 1.0) < 1e-4

def test_polynomial():
    """Проверка интеграла полинома x^2 на [0, 2]"""
    result = integrate(lambda x: x**2, 0, 2, n_iter=100000)
    expected = 8/3  # ≈ 2.6666667
    assert abs(result - expected) < 1e-4

def test_iterations_independence():
    """Результат не должен меняться кардинально при увеличении итераций"""
    res1 = integrate(math.sin, 0, math.pi, n_iter=1000)
    res2 = integrate(math.sin, 0, math.pi, n_iter=10000)
    assert abs(res1 - res2) < 0.01  # Разница менее 1%

def test_invalid_args():
    """Проверка обработки некорректных аргументов"""
    with pytest.raises(ValueError):
        integrate(math.cos, 5, 0, n_iter=1000)  # a > b
    with pytest.raises(ValueError):
        integrate(math.cos, 0, 1, n_iter=0)     # n_iter <= 0