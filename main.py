import equation_generator as eg
import equation_solver as es
import tests_generator as tg
import equation as e
from some_stuff import *

import numpy as np
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
    y0 = 0

    with open("tests.txt", 'w') as ost:
        for i in range(0, 100):
            equation = eg.gen(a_range, b_range, precision, ft_max_depth,
                              true_with_chance(chance_homogenous),
                              true_with_chance(chance_separable))
            integrated = es.integrate_eq(equation, t_vec, y0)
            ost.write(f"{equation}\n")
