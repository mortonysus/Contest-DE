from some_stuff import *
import numpy as np
import equation as eq
import sympy as smp


# Возвращает true с переданной вероятностью [0:1].
def true_with_chance(chance):
    return numpy.random.choice([True, False], p=[chance, 1 - chance])


# Возвращает результат применения случайного бинарного оператора.
def rnd_op(a, b):
    return np.random.choice([a + b, a - b, a * b, a / b, a ** b])


# Возвращает случайную тригонометрическую функцию (как насчет гаверсинуса?).
def rnd_trig_func():
    return np.random.choice([smp.sin, smp.asin, smp.sinh, smp.asinh,
                             smp.cos, smp.acos, smp.cosh, smp.acosh,
                             smp.tan, smp.atan, smp.tanh, smp.atanh,
                             smp.cot, smp.acot, smp.coth, smp.acoth,
                             smp.sec, smp.asec, smp.sech, smp.asech,
                             smp.csc, smp.acsc, smp.csch, smp.acsch,
                             ])


# Возвращает случайную алгебраическую функцию.
def rnd_func():
    return np.random.choice([rnd_trig_func(), smp.sqrt, smp.exp, smp.log, smp.cbrt])


# Генерирует выражение зависящее от t.
# depth - максимальная глубина рекурсии(размер выражения на выходе.
# TODO:
# *) Есть исчезающе-малый шанс на генерацию чего то невалидного, надо проверять валидность для точек.
def rnd_ft(depth):
    t = smp.Symbol('t')
    if depth <= 0:
        return t
    # Выбираем:
    #   Добавить слагаемое / множитель
    #   Увеличить вложенность
    #   Добавить и увеличить
    #   Ничего не делать
    # Теоретически это даст возможность получить любые комбинации выражений с глубиной вложенности не больше заданной
    dive = true_with_chance(0.5)
    operator = true_with_chance(0.5)

    # Возможно это все достаточно неприлично.
    if dive and not operator:
        return (rnd_func())(rnd_ft(depth - 1))
    if not dive and operator:
        return rnd_op((rnd_func())(t), rnd_ft(depth - 1))
    if dive and operator:
        return rnd_op((rnd_func())(rnd_ft(depth - 1)), rnd_ft(depth - 1))
    if not operator and not dive:
        return rnd_func()(t)


def make_from_y(a2, b2, y):
    # f(t) = a1*y' +b1*y
    # y' = (-b1/a1)*y + (1/a1)*f(t)
    # y' = a2*y + b2*f(t)
    a1 = smp.Rational(1, b2).limit_denominator(100)
    b1 = smp.Rational(-a2, b2).limit_denominator(100)
    dy = smp.simplify(smp.diff(y))
    ft = smp.simplify(a1 * dy + b1 * y)
    return eq.Equation(a2, b2, ft, y)


def gen(a, b, ft_depth, homogenous, separable):
    y = smp.simplify(rnd_ft(ft_depth))
    return make_from_y(a, b, y)
