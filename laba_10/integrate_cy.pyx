import cython
from libc.math cimport sin, cos, exp, log, sqrt

# Тип указателя на C-функцию: double -> double
ctypedef double (*func_ptr)(double)

@cython.cdivision(True)
cdef double _integrate_c(func_ptr f, double a, double b, int n_iter) noexcept:
    cdef double acc = 0.0
    cdef double step = (b - a) / n_iter
    cdef int i
    cdef double x
    for i in range(n_iter):
        x = a + i * step
        acc += f(x) * step
    return acc

# Публичные функции — одна под каждую известную f
def integrate_sin(double a, double b, int n_iter=100_000):
    if n_iter <= 0:
        raise ValueError("n_iter должен быть положительным")
    if a >= b:
        raise ValueError("a должен быть меньше b")
    return _integrate_c(sin, a, b, n_iter)

def integrate_cos(double a, double b, int n_iter=100_000):
    if n_iter <= 0:
        raise ValueError("n_iter должен быть положительным")
    if a >= b:
        raise ValueError("a должен быть меньше b")
    return _integrate_c(cos, a, b, n_iter)

def integrate_exp(double a, double b, int n_iter=100_000):
    if n_iter <= 0:
        raise ValueError("n_iter должен быть положительным")
    if a >= b:
        raise ValueError("a должен быть меньше b")
    return _integrate_c(exp, a, b, n_iter)

# Для полинома x^2
cdef double _f_x2(double x):
    return x * x

def integrate_x2(double a, double b, int n_iter=100_000):
    if n_iter <= 0:
        raise ValueError("n_iter должен быть положительным")
    if a >= b:
        raise ValueError("a должен быть меньше b")
    return _integrate_c(_f_x2, a, b, n_iter)

# Для 2*x
cdef double _f_2x(double x):
    return 2.0 * x

def integrate_2x(double a, double b, int n_iter=100_000):
    if n_iter <= 0:
        raise ValueError("n_iter должен быть положительным")
    if a >= b:
        raise ValueError("a должен быть меньше b")
    return _integrate_c(_f_2x, a, b, n_iter)

def integrate_generic(object f, double a, double b, int n_iter=100_000):
    """Используется ТОЛЬКО если f — произвольная Python-функция."""
    if n_iter <= 0:
        raise ValueError("n_iter должен быть положительным")
    if a >= b:
        raise ValueError("a должен быть меньше b")
    cdef double acc = 0.0
    cdef double step = (b - a) / n_iter
    cdef int i
    cdef double x
    cdef object local_f = f
    for i in range(n_iter):
        x = a + i * step
        acc += local_f(x) * step
    return acc


@cython.cdivision(True)
cpdef double integrate_c_cos_nogil(double a, double b, int n_iter=100_000) nogil:
    """
    Интегрирует cos(x) на [a, b] без удержания GIL.
    Полностью безопасен для многопоточности.
    """
    cdef double acc = 0.0
    cdef double step = (b - a) / n_iter
    cdef int i
    cdef double x

    for i in range(n_iter):
        x = a + i * step
        acc += cos(x) * step

    return acc


def integrate_cos_nogil(double a, double b, int n_iter=100_000):
    if n_iter <= 0:
        raise ValueError("n_iter должен быть положительным")
    if a >= b:
        raise ValueError("a должен быть меньше b")
    return integrate_c_cos_nogil(a, b, n_iter)