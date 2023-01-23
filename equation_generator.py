import numpy as np
import Equation as eq
import sympy as smp


# Возвращает true с переданной вероятностью [0:1].
def true_with_chance(chance):
    return np.random.choice([True, False], p=[chance, 1 - chance])


# Возвращает результат применения случайного бинарного оператора.
def rnd_op(a, b):
    return np.random.choice([a + b, a - b, a * b])


# Возвращает выражение возведенное в случайную степень от 2 до 5
def power(expr):
    return expr ** np.random.randint(2, 5)


# Возвращает случайную алгебраическую функцию.
def rnd_func():
    return np.random.choice([smp.sin, smp.cos, smp.exp, power])


# Генерирует выражение зависящее от t.
# depth - максимальная глубина рекурсии(размер выражения на выходе.
def rnd_expr(depth, sym):
    if depth <= 0:
        return sym

    if true_with_chance(0.5):
        return rnd_op((rnd_func())(sym * round(np.random.uniform(1, 10), 2)), rnd_expr(depth - 1, sym))
    return rnd_func()(sym * round(np.random.uniform(1, 10), 2)) * round(np.random.uniform(1, 10, 2))


def gen(a_range, b_range, depth, homogenous=False, separable=False):
    a = np.random.uniform(*a_range)
    b = np.random.uniform(*b_range)
    c = np.random.uniform(1, 1)  # Константа для частного решения

    e = eq.Equation(a, b, rnd_expr(depth, smp.Symbol('t')))
    e.definite(c)

    return e


if __name__ == '__main__':
    e = gen((1, 2), (4, 5), 1)
    print(e)
    print(e.a)
    print(e.b)
