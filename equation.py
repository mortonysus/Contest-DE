import sympy as smp


# ODE in format: y' = a*y + b*f(t)
class Equation:
    homogenous, separable = False, False

    # a -
    # b -
    # ft -
    def __init__(self, a, b, ft, solve):
        self.ft = ft
        self.solve = solve
        self.a, self.b = a, b

    def __str__(self):
        y = smp.Symbol('y')
        return f"y' = {smp.simplify(self.a * y + self.b * self.ft)}"
