import os
import numpy as np
import equation_generator as eg
from random import randint
from configs import *
from Process import *


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


def make_folder(path):
    if not os.path.exists(path):
        os.makedirs(path)


def make_folders(set_n):
    general_path = "tests"
    make_folder(general_path)
    make_folder(os.path.join(general_path, f"set{set_n}", "tests"))
    make_folder(os.path.join(general_path, f"set{set_n}", "answers"))


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


def gen_test(cfg, set_n, test_n):
    equation = eg.gen(cfg["depth"])
    picard = slv.picard(cfg["iters"], equation.right_part(), cfg["t0"],
                        cfg["y0"])

    answer = float(picard.subs('t', cfg["tk"]).evalf())  # conversion exception
    if abs(answer) > cfg["max"]:
        raise Exception(f"Too big answer value in equation {equation}, regenerating equation...")

    output_test(cfg, set_n, test_n, equation)
    output_answer(set_n, test_n, answer)

    print(f"{test_n})")
    print(f"\tEquation: {equation}")
    print(f"\ty({cfg['t0']}) = {cfg['t0']}")
    print(f"\tIterations: {cfg['iters']}")
    print(f"\ty_{cfg['iters']} = {picard}")
    print(f"\ty_{cfg['iters']}({cfg['tk']}) = {answer}")


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
