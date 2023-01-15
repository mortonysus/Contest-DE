import numexpr as ne
import numpy as np
import math
import equation as e


class test:
    def __init__(self, equation, solution, t_vec, c):
        self.equation = equation
        self.solution = solution
        self.t_vec = t_vec
        self.c = c

    def __str__(self):
        ret = ""
        ret += self.equation.ft + '\n'
        ret += str(self.t_vec.size) + '\n'
        c = 2
        for t in self.t_vec:
            ret += str(t) + ' ' + str(ne.evaluate(self.solution, {"t": t, "c": c, "e": math.e})) + '\n'
        ret += f"answer: {self.equation.a} {self.equation.b}"
        return ret + '\n'


if __name__ == '__main__':
    t0 = 0
    tn = 10
    t_size = 100
    t_vec = np.linspace(t0, tn, t_size)
    c = 2
    with open("tests.txt", 'w') as ost:
        ost.write(str(test(e.Equation(0, 0, "0"),
                           "c",
                           t_vec, c)) + '\n')  # y' = 0
        ost.write(str(test(e.Equation(0, 1, "t"),
                           "(t**2)/2 + c",
                           t_vec, c)) + '\n')  # y' = t
        ost.write(str(test(e.Equation(1, 1, "t"),
                           "c*(e**t) - t - 1",
                           t_vec, c)) + '\n')  # y' = y + t
        ost.write(str(test(e.Equation(25, 1, "t"),
                           "(c*(e**(25*t))-25*t -1)/625",
                           t_vec, c)) + '\n')  # y' = 25y + t
        ost.write(str(test(e.Equation(15, -6, "t"),
                           "(c*(e**(15*t))+30*t +2)/75",
                           t_vec, c)) + '\n')  # y' = 15y - 6t
        ost.write(str(test(e.Equation(1, 1, "sin(t)"),
                           "(-1/2)*sin(t) -(1/2)*cos(t) + c*(e**t)",
                           t_vec, c)) + '\n')  # y' = y + sin(t)
        ost.write(str(test(e.Equation(-6, 7, "cos(t)"),
                           "(7/37)*sin(t)+(42/37)*cos(t) + c/(e**(6*t))",
                           t_vec, c)) + '\n')  # y' = -6y + 7cos(t)
        ost.write(str(test(e.Equation(0, -11.78, "log(t) + sqrt(t)"),
                           "(-589/50)*(t*log(t)) - (589/75)*(t**(3/2)) + (589/50) + c",
                           t_vec, c)) + '\n')  # y' = -11.78(ln(t) + sqrt(t))
        ost.write(str(test(e.Equation(2.37, -17.93, "t**2"),
                           "c*(e**(2.37*t)) + (1793/237)*(t**2) + (358600/56169)*t + (35860000/13312053)",
                           t_vec, c)) + '\n')  # y' = 2.37y - 17.93t^2
        ost.write(str(test(e.Equation(-5.33, -13.6, "sin(2t)"),
                           "(-724880/324089)*sin(2*t) + (272000/324089)*cos(2*t) + c/(e**(5.33*t))",
                           t_vec, c)) + '\n')  # y' = -5.33y -13.6sin(2t)
