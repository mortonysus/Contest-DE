import numpy as np
import Equation as eq
import sympy as smp


# Возвращает случайную тригонометрическую функцию.
def rnd_trig_func():
    return np.random.choice([smp.sin, smp.asin, smp.sinh, smp.asinh,
                             smp.cos, smp.acos, smp.cosh, smp.acosh,
                             smp.tan, smp.atan, smp.tanh, smp.atanh,
                             smp.cot, smp.acot, smp.coth, smp.acoth,
                             smp.sec, smp.asec, smp.sech, smp.asech,
                             smp.csc, smp.acsc, smp.csch, smp.acsch,
                             ])

# Генерация неоднородных уравнений
def make_from_y(a2, b2, y):
    # f(t) = a1*y' +b1*y
    # y' = (-b1/a1)*y + (1/a1)*f(t)
    # y' = a2*y + b2*f(t)
    a1 = smp.Rational(1, b2).limit_denominator(100)
    b1 = smp.Rational(-a2, b2).limit_denominator(100)
    dy = smp.simplify(smp.diff(y))
    ft = smp.simplify((a1 * dy + b1 * y))
    return eq.Equation(a2, b2, ft, y)


# Генерация однородных уравнений, a2 != 0, f(t) == 0
def make_homogeneous(a2, b2, y):
    t = smp.Symbol('t')
    # y' = -a2y
    # y = c * e^(a1x)
    # ft = 0
    ft = smp.simplify(t - t)
    y = smp.exp(a2 * t)
    return eq.Equation(a2, b2, ft, y)


# Генерация уравнений с разделяющимися переменными, a2 == 0, f(t) != 0
def make_separate(a2, b2, y):
    t = smp.Symbol('t')
    a2 = smp.simplify(t - t)
    ft = y
    y = smp.integrate(ft * b2, t)
    return eq.Equation(a2, b2, ft, y)


# Генерация однородных уравнений с разделяющимися переменными, a2 == 0, f(t) == 0
def make_separate_homogeneous(a2, b2, y):
    t = smp.Symbol('t')
    c = smp.Symbol('c')
    a2 = smp.simplify(t - t)
    y = smp.numer(np.random.randint(10) + 1)
    ft = smp.simplify(t - t)
    return eq.Equation(a2, b2, ft, y)


# Пока не получается нормально генерировать функцию так чтобы потом интегрировалось,
# но мы исправим и будут более интересные функции. (Разработка в ветке main)
def gen(depth, homogenous, separable):
    y = rnd_trig_func()(smp.Symbol('t'))

