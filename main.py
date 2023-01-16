import equation_generator as eg
import equation_solver as es
from some_stuff import *
import numpy as np
import sympy as smp
from matplotlib import pyplot as plt

if __name__ == '__main__':
    chance_homogenous = 0.03
    chance_separable = 0.50
    ft_max_depth = 2

    a_range = (-10, 10)
    b_range = (-20, -10)
    precision = 2

    t0 = 0
    tn = 10
    t_size = 100
    t_vec = np.linspace(t0, tn, t_size)

    with open("tests.txt", 'w') as ost:
        for i in range(0, 10):
            a = smp.Rational(rnd_non_zero(a_range, precision)).limit_denominator(100)
            b = smp.Rational(rnd_non_zero(b_range, precision)).limit_denominator(100)
            equation = eg.gen(a, b, ft_max_depth,
                              true_with_chance(chance_homogenous),
                              true_with_chance(chance_separable))
            ost.write(f"{equation}\n")
            ost.write(f"y = {equation.solve}\n")
            ost.write(f"ft = {equation.ft}\n")


