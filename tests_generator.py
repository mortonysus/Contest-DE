import os
import numpy as np
import equation_generator as eg
from random import randint


# Возвращает список точек функции для диапазона,
# если функция:
# - принимает комплексные значения,
# - невычислима хотя бы в одной точке
# - принимает слишком большие значения - вернет []
def discretize(y, t_vec, max_value):
    ret = []
    try:
        for t in t_vec:
            value = float(y.subs('t', t))
            if value > max_value:
                return []
            ret.append(tuple([t, value]))
        return ret
    except:
        return []


def make_folders(config):
    if not os.path.exists(config["tests_path"]):
        os.makedirs(config["tests_path"])
    if not os.path.exists(config["answers_path"]):
        os.makedirs(config["answers_path"])


def valid_equation(cfg):
    # Дробные коэффициенты будут.
    a = randint(*cfg["a_range"])
    b = randint(*cfg["b_range"])
    if cfg["distribution"] == "random":
        t_vec = np.sort([np.random.uniform(cfg["t0"], cfg["tn"]) for point in range(cfg["points"])])
    elif cfg["distribution"] == "uniform":
        t_vec = np.linspace(cfg["t0"], cfg["tn"], cfg["points"])
    else:
        raise Exception(f"unknown distribution mode: {cfg['distribution']}")
    while True:
        equation = eg.gen(a, b, cfg["homogenous"], cfg["separable"])
        points = discretize(equation.y, t_vec, cfg["max_value"])
        if points != []:
            break
    return equation, points


def output_test(cfg, test_n, equation, points):
    with open(os.path.join(cfg["tests_path"], f"test{test_n}.test"), 'w') as ost:
        ost.write(str(equation.ft) + '\n')
        ost.write(str(cfg["points"]) + '\n')
        for t, y in points:
            ost.write(f"{t} {y}\n")


def output_answer(cfg, test_n, equation):
    with open(os.path.join(cfg["answers_path"], f"test{test_n}.answer"), 'w') as ost:
        ost.write(f"{equation.a} {equation.b}\n")
        ost.write(f"{equation}\n")
        ost.write(f"y = {equation.y}\n")
        ost.write(f"ft = {equation.ft}\n")


# В дальнейшем будет в отдельном файле.
test_configs = [
    {
        "count": 10,
        "depth": 1,
        "t0": 10,
        "tn": 20,
        "points": 11,
        "a_range": (-10, -1),
        "b_range": (-10, -1),
        "max_value": 10 ** 6,
        "tests_path": "tests",
        "answers_path": os.path.join("tests", "answers"),
        "separable": False,
        "homogenous": False,
        "distribution": "random"
    }
]

if __name__ == '__main__':
    for cfg in test_configs:
        make_folders(cfg)
        for test_n in range(0, cfg["count"]):
            equation, points = valid_equation(cfg)
            output_test(cfg, test_n, equation, points)
            output_answer(cfg, test_n, equation)
