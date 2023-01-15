# То что может понадобиться в разных местах

import numpy
import numexpr


# Возвращает true с переданной вероятностью [0:1].
def true_with_chance(chance):
    return numpy.random.choice([True, False], p=[chance, 1 - chance])


# Вернет число с заданной точностью.
def set_precision(number, precision):
    return float(f"%.{precision}f" % number)



def make_second(n):
    if n >= 0:
        return "+ " + str(n)
    return "- " + str(abs(n))