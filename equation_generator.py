from some_stuff import *
import numpy as np
import equation as eq


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
    return np.random.choice(["+", "-", "*", "/", "**"])


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


def gen(a_range, b_range, precision, ft_depth, homogenous, separable):
    a = 0 if separable else rnd_non_zero(a_range, precision)
    b = 0 if homogenous else rnd_non_zero(b_range, precision)
    ft = "0" if homogenous else simplify(gen_ft(ft_depth))
    return eq.Equation(a, b, ft)
