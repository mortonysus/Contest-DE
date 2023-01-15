import numpy as np
import scipy as scp
from some_stuff import *
import equation_generator as eg


# Дискретное решение задачи Коши.
# dy/dt = foo(y,t) -> [...]
# y0 - параметр для решения задачи коши - FOO(t0) = y0
# t_vec - точки для которых будет найдено решение
def integrate(foo, y0, t_vec):
    return np.array([a[0] for a in scp.integrate.odeint(foo, y0, t_vec)])


def make_yt_expression(ab_equation):
    right_part = ab_equation[ab_equation.find("=") + 2:]
    return right_part.replace("y", "*y").replace("(", "*(", 1)


def integrate_ab_equation(ab_equation, t_vec, y0, precision):
    yt_expression = make_yt_expression(ab_equation)
    return integrate(lambda y, t: numexpr.evaluate(yt_expression), y0, t_vec)


def integrate_a1a0_equation(a1a0_equation, t_vec, y0, precision):
    ab_equation = eg.make_ab_equation(a1a0_equation, precision)
    return integrate_ab_equation(ab_equation, t_vec, y0, precision)
