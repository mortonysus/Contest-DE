import os
import numpy as np
import equation_generator as eg
from random import randint
from configs import *
from Process import *


# Вычисляет функцию в точках,
# Бросает исключения если функция:
# - принимает комплексные значения,
# - невычислима хотя бы в одной точке
# - принимает слишком большие значения
def discretize(y, t_vec, max_value):
    ret = []
    for t in t_vec:
        value = float(y.subs('t', t))
        if value > max_value:
            raise Exception(f"Too big value for function {y} in t_vec, regenerating equation...")
        ret.append(tuple([t, value]))
    return ret


def make_folder(path):
    if not os.path.exists(path):
        os.makedirs(path)


def make_folders(set_n):
    general_path = "tests"
    make_folder(general_path)
    make_folder(os.path.join(general_path, f"set{set_n}", "tests"))
    make_folder(os.path.join(general_path, f"set{set_n}", "answers"))


def output_test(cfg, set_n, test_n, equation, points):
    with open(os.path.join("tests", f"set{set_n}", "tests", f"test{test_n}.test"), 'w') as ost:
        ost.write(f"{equation.f}\n")
        ost.write(f"{cfg['points']}\n")
        for t, y in points:
            ost.write(f"{t} {y}\n")


# На самом деле ответ может быть бесполезен потому что правильных ответов может быть несколько
def output_answer(set_n, test_n, a, b):
    with open(os.path.join("tests", f"set{set_n}", "answers", f"test{test_n}.answer"), 'w') as ost:
        ost.write(f"{a} {b}\n")


def gen_test(cfg, set_n, test_n):
    # Генерируем уравнение с параметрами из конфига
    equation = eg.gen(cfg["a_range"],
                      cfg["b_range"],
                      cfg["depth"],
                      cfg["homogenous"],
                      cfg["separable"]
                      )
    # Генерируем точки для частного решения уравнения
    if cfg["distribution"] == "random":
        t_vec = np.sort([np.random.uniform(cfg["t0"], cfg["tn"]) for point in range(cfg["points"])])
    elif cfg["distribution"] == "uniform":
        t_vec = np.linspace(cfg["t0"], cfg["tn"], cfg["points"])
    else:
        raise Exception(f"unknown distribution mode: {cfg['distribution']}")

    points = discretize(equation.y_part, t_vec, cfg["max_value"])

    output_test(cfg, set_n, test_n, equation, points)
    output_answer(set_n, test_n, equation.a, equation.b)

    print(f"{test_n})")
    print(f"\tEquation: {equation}")


def gen_test_wrapper(test_n, set_n):
    gen = Process(target=gen_test, args=(configs[set_n - 1], set_n, test_n))
    gen.start()
    gen.join(timeout=configs[set_n - 1]['timeout'])
    if gen.exception:
        raise Exception(gen.exception[0])
    if gen.is_alive():
        gen.terminate()
        raise Exception("Too long generation, regenerating...")


def gen_set(set_n):
    make_folders(set_n)
    test_n = 1
    while test_n != configs[set_n - 1]["count"] + 1:
        try:
            gen_test_wrapper(test_n, set_n)
        except Exception as e:
            print(e)
            continue
        test_n += 1


if __name__ == '__main__':
    print(f"Generating ({len(configs)}) sets of tests.")
    for set_n in range(1, len(configs) + 1):
        print(f"\nTest set #{set_n}")
        gen_set(set_n)
