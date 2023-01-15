# ODE in format: y' = a*y + b*f(t)
class Equation:
    homogenous, separable = False, False

    def __init__(self, a, b, ft):
        if b == 0 or ft == "0":
            ft = "0"
            self.homogenous = True
        if a == 0:
            self.separable = True

        self.ft = ft
        self.a, self.b = a, b

    def __str__(self):
        if self.separable and self.homogenous:
            return "y' = 0"
        if not self.separable and self.homogenous:
            return f"y' = {self.a}*y"
        if self.separable and not self.homogenous:
            return f"y' = {self.b}*({self.ft})"
        if not self.separable and not self.homogenous:
            return f"y' = {self.a}*y {'+' if self.b > 0 else '-'} {abs(self.b)}*({self.ft})"
