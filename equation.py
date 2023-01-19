import sympy as smp


# ODE in format: y' = a*y + b*f(t)
class Equation:
    def __init__(self, a, b, ft, y):
        self.ft = ft
        self.y = y
        self.a, self.b = a, b

    def __str__(self):
        y = smp.Symbol('y')
        return f"y' = {smp.simplify(self.a * y + self.b * self.ft)}"
