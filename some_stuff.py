# То что может понадобиться в разных местах

import numpy
import random


# Возвращает true с переданной вероятностью [0:1].
def true_with_chance(chance):
    return numpy.random.choice([True, False], p=[chance, 1 - chance])


# Вернет число с заданной точностью.
def set_precision(number, precision):
    return float(f"%.{precision}f" % number)


# Случайное число из диапазона [a,b] но не 0
def rnd_non_zero(n_range, precision):
    n = 0
    while n == 0:
        n = set_precision(random.randint(n_range[0], n_range[1]), precision)
    if n.is_integer():
        n = int(n)  # Чтобы не было лишних нулей
    return n
