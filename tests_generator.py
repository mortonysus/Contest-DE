import numpy as np
import os
from some_stuff import *
import sympy as smp
import equation_generator as eg

if __name__ == '__main__':
    tests_path = "tests"
    tests_answers_path = os.path.join(tests_path, "answers")
    if not os.path.exists(tests_path):
        os.makedirs(tests_path)
    if not os.path.exists(tests_answers_path):
        os.makedirs(tests_answers_path)

    test_configs = [
        {
            "count": 10,
            "depth": 2,
            "t0": 0,
            "tn": 10,
            "points": 100,
            "int_ab": True,
            "a_range": (-10, 10),
            "b_range": (-20, -10),
            "ab_precision": 2
        }
    ]

    for test_config in test_configs:
        for test_number in range(0, test_config["count"]):
            a = smp.Rational(rnd_non_zero(test_config["a_range"], test_config["ab_precision"])).limit_denominator(100)
            b = smp.Rational(rnd_non_zero(test_config["b_range"], test_config["ab_precision"])).limit_denominator(100)
            equation = eg.gen(a, b, test_config["depth"], False, False)
            with open(os.path.join(tests_path, f"test{test_number}.test"), 'w') as ost:
                ost.write(str(equation.ft) + '\n')
                for t in np.linspace(test_config["t0"], test_config["tn"], test_config["points"]):
                    ost.write(f"{t} {equation.y.subs('t', t).evalf()}\n")
            with open(os.path.join(tests_answers_path, f"test{test_number}.answer"), 'w') as ost:
                ost.write(f"{equation.a} {equation.b}\n")
                ost.write(f"{equation}\n")
                ost.write(f"y = {equation.y}\n")
                ost.write(f"ft = {equation.ft}\n")
