import equation_generator as eg
import equation_solver as es

from some_stuff import *
import numpy as np
from matplotlib import pyplot as plt
import math

def exact_solution_function(t, c):
    return -(1 / 4) * (math.e ** (-2 * t)) * (c ** 2 - 3 * math.e ** (2 * t) + 6 * t * math.e ** (2 * t))

if __name__ == '__main__':
    chance_homogenous = 0.03
    chance_separable = 0.50
    ft_max_depth = 2

    a1_range = (-10, 10)
    a0_range = (-20, -10)
    precision = 2

    t0 = 0
    tn = 10
    t_size = 100
    t_vec = np.linspace(t0, tn, t_size)
    y0 = 0

    a1a0_equation = "-0.33y' - 0.66y = t"
    integrated = es.integrate_a1a0_equation(a1a0_equation, t_vec, y0, precision)
    calculated = np.array([exact_solution_function(t, math.sqrt(3)) for t in t_vec])
    plt.plot(range(t0, calculated.size), calculated)
    plt.plot(range(t0, integrated.size), integrated)
    plt.show()
    # with open("tests.txt", 'w') as ost:
    #     for i in range(0, 1):
    #         a1a0_equation = eg.gen_a1a0_equation(a1_range, a0_range, precision, ft_max_depth,
    #                                              true_with_chance(chance_homogenous),
    #                                              true_with_chance(chance_separable))
    #         print(a1a0_equation)
    #         integrated = es.integrate_a1a0_equation(a1a0_equation, t_vec, y0, precision)
    #         plt.plot(range(t0, integrated.size), integrated)
    #         plt.show()
    #         ost.write(a1a0_equation[:] + '\n')
    #         print()
