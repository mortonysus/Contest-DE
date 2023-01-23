import numpy as np
import sympy as smp
from sympy.integrals.risch import NonElementaryIntegral


# ODE in format: y' = a*y + b*f(t)
class Equation:
    def solve(self, a):
        # Общее решение линейного уравнения первого порядка с постоянными коэффициентами. Нужно решить в элементарных
        # функциях, к сожалению опция risch=True в sympy.integrate которая под это сделана не позволяет интегрировать
        # многие штуки. Поэтому если f плохая функция или a плохой параметр - то просто зависнет.
        t, c = smp.Symbol('t'), smp.Symbol('c')
        integral = smp.integrate(self.f / smp.exp(a * t), t)
        y = self.b * smp.exp(a * t) * (integral + c)

        if isinstance(integral, NonElementaryIntegral):  # Это не всегда сработает потому что sympy пока немного тупой.
            raise Exception(f"Non elementary integral: {integral}")

        try:
            float(y.subs({'t': 0, 'c': 0}).evalf())  # Проверка на вычислимость (функцию ошибок и прочее в бан)
        except TypeError as e:
            raise Exception(f"Non elementary integral: {integral}")

        return y

    def right_part(self):
        return self.a * smp.Symbol('y') + self.b * self.f

    def check_invariant(self):
        dydt = smp.diff(self.y_gen, smp.Symbol('t'))
        substituted = self.right_part().subs('y', self.y_gen)
        check_sum = smp.simplify(dydt - substituted)
        if check_sum != smp.Rational(0):
            print(dydt)
            print(substituted)
            print(check_sum)
            raise Exception(f"Equation invariant failed {check_sum}")

    def __init__(self, a, b, f):
        self.a, self.b, self.f = a, b, f

        # Решение при истинном a
        self.y_gen = self.solve(a)  # y = f(t,c)
        # Проверка при других a (чтобы работал градиентный спуск)
        self.solve(-a)
        self.solve(a / 2)
        self.solve(-a / 2)

        self.check_invariant()

    def definite(self, c):
        # Определяем частное решение
        self.y_part = self.y_gen.subs('c', c)

    def __str__(self):
        return f"y' = {self.right_part()}"


if __name__ == '__main__':
    try:
        t = smp.Symbol('t')
        e = Equation(2, -2, smp.sin(t))
        e.definite(1)
        print(e)
        print(f"y_gen = {smp.simplify(e.y_gen)}")
        print(f"y_part = {smp.simplify(e.y_part)}")

    except Exception as ex:
        print(ex)
