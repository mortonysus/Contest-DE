# LEGACY (LOL)

import numpy as np
import scipy as scp
import math
import numexpr as ne
from some_stuff import *


# Функция решения из примера для y' + 2y = -3t
def example_exact_solution_function(t, c):
    return -(1 / 4) * (math.e ** (-2 * t)) * (c ** 2 - 3 * math.e ** (2 * t) + 6 * t * math.e ** (2 * t))
    # calculated = np.array([example_exact_solution_function(t, math.sqrt(3)) for t in t_vec])
    # Для y(0) = 0 с = sqrt(3)


# Дискретное решение задачи Коши.
# dy/dt = foo(y,t) -> [...]
# y0 - параметр для решения задачи коши - FOO(t0) = y0
# t_vec - точки для которых будет найдено решение
def integrate(foo, y0, t_vec):
    return np.array([a[0] for a in scp.integrate.odeint(foo, y0, t_vec)])


# Решить задачу Коши для диффура вида y' = f(y,t) на промежутке t_vec при y(t0) = y0
def integrate_eq(equation, t_vec, y0):
    return integrate(lambda y, t: ne.evaluate(equation.ft), y0, t_vec)
