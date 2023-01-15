import random
import numpy as np
from some_stuff import *


# Возвращает случайное название тригонометрической функции (как насчет гаверсинуса?).
def rnd_trig_func_name():
    trig_func = np.random.choice(["sin", "cos", "tan"])
    if true_with_chance(0.5):
        trig_func += "h"
    if true_with_chance(0.5):
        trig_func = "arc" + trig_func
    return trig_func


# Возвращает случайное название алгебраической функции.
def rnd_func_name():
    return np.random.choice([rnd_trig_func_name(), "sqrt", "exp", "log"])


# Возвращает случайный бинарный оператор.
def rnd_op_sym():
    return numpy.random.choice(["+", "-", "*", "/", "**"])


# Генерирует строку, которая содержит "случайное" математическое выражение, зависящее от t.
# depth - максимальная глубина рекурсии(размер выражения на выходе.
# Пока возникают перлы в виде ln(t - t) итд,
# TODO:
# 1) Есть проблема с нулями в неправильных местах (t-t).
# 2) Выражение должно быть вычислимо для диапазона (который надо передавать).
# 3) Добавить числовые коэффициенты.
def gen_ft(depth):
    if depth <= 0:
        return "t"

    # Выбираем:
    #   Добавить слагаемое / множитель
    #   Увеличить вложенность
    #   Добавить и увеличить
    #   Ничего не делать
    # Теоретически это даст возможность получить любые комбинации выражений с глубиной вложенности не больше заданной
    dive = true_with_chance(0.5)
    operator = true_with_chance(0.5)

    # Возможно это все достаточно неприлично.
    if dive and not operator:
        return f"{rnd_func_name()}({gen_ft(depth - 1)})"  # Тут точно не нужны внешние скобки
    if not dive and operator:
        return f"({rnd_func_name()}(t) {rnd_op_sym()} {gen_ft(depth - 1)})"
    if dive and operator:
        return f"({rnd_func_name()}({gen_ft(depth - 1)}) {rnd_op_sym()}  {gen_ft(depth - 1)})"
    if not operator and not dive:
        return "t"  # Тут точно не нужны внешние скобки


# Упростить артефакты генерации f(t) (Хотя бы чуть-чуть).
def simplify(ft):
    return ft. \
        replace("(t - t)", "(0)"). \
        replace("(t / t)", "(1)"). \
        replace("(t * t)", "(t ** 2)"). \
        replace("(t + t)", "(2 * t)")


# Случайное число из диапазона [a,b] но не 0
def rnd_non_zero(n_range, precision):
    n = 0
    while n == 0:
        n = set_precision(random.uniform(n_range[0], n_range[1]), precision)
    if n.is_integer():
        n = int(n)  # Чтобы не было лишних нулей
    return n


# Генерирует строку, которая содержит диффур вида a1y' + a0y = f(t)
def gen_a1a0_equation(a1_range, a0_range, precision, ft_depth, is_homogenous, is_separable):
    if is_homogenous:
        ft = "0"
    else:
        ft = "t"
        while ft == "t":
            ft = simplify(gen_ft(ft_depth))

    a1 = rnd_non_zero(a1_range, precision)  # Нужно выбрать a1 из диапазона, но не 0 (иначе диффур не получится)
    if is_separable:
        return f"{a1}y' = {ft}"

    a0 = rnd_non_zero(a0_range, precision)
    return f"{a1}y' {make_second(a0)}y = {ft}"


# Преобразовать линейное уравнение первого порядка в формате:
# [a1y' sign(a0) abs(a0)y = f(t) ->
# y' = ay + bf(t)
def make_ab_equation(a1a0_equation, precision):
    if a1a0_equation.find("y ") == -1:
        separable_equation = True
        a0 = 0
    else:
        separable_equation = False
        a0 = float((a1a0_equation[a1a0_equation.find("y'") + 3:a1a0_equation.find("y ")]).replace(' ', ''))

    a1 = float((a1a0_equation[:a1a0_equation.find("y'")]))
    ft = a1a0_equation[a1a0_equation.find("=") + 2:]
    if ft == "0":
        homogenous_equation = True
    else:
        homogenous_equation = False

    b = set_precision(1 / a1, precision)
    ret = "y' = "
    if not separable_equation:
        a = set_precision(-a0 / a1, precision)
        ret += f"{a}y"
        if not homogenous_equation:
            ret += f" {make_second(b)}({ft})"
    else:
        if homogenous_equation:
            ret += "0"
        else:
            ret += f"{b}({ft})"
    return ret


def gen_ab_equation(a1_range, a0_range, precision, ft_depth, is_homogenous, is_separable):
    return make_ab_equation(gen_a1a0_equation(a1_range, a0_range, precision, ft_depth, is_homogenous, is_separable),
                            precision)
