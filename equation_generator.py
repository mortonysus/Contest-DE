import random
import numexpr
import numpy

from some_stuff import *


# Возвращает случайное название тригонометрической функции (как насчет гаверсинуса?).
def choice_trig_function():
    base_functions = ["sin", "cos", "tan"]
    func = numpy.random.choice(base_functions)
    if true_with_chance(0.5):
        func += "h"
    if true_with_chance(0.5):
        func = "arc" + func
    return func


# Возвращает случайное название математической функции.
def choice_function():
    return numpy.random.choice([choice_trig_function(), "sqrt", "exp", "ln"])


# Возвращает случайный бинарный оператор
def choice_operator():
    return numpy.random.choice(["+", "-", "*", "/", "**"])


# Генерирует строку, которая содержит "случайное" математическое выражение, зависящее от t.
# Чтобы увеличить веселость выражения на выходе - нужно поднять depth
# Пока возникают перлы в виде ln(t - t) итд,
# можно попытаться от них избавиться или проверять выражение на валидность в другом месте
# можно добавить чиселок, но суть не в чиселках
def gen_ft(depth):
    # Выбираем:
    #   Добавить слагаемое / множитель
    #   Увеличить вложенность
    #   Добавить и увеличить
    #   Ничего не делать

    # Теоретически это даст возможность получить любые комбинации выражений с глубиной вложенности не больше заданной
    if depth <= 0:
        return "t"

    dive = true_with_chance(0.5)
    operator = true_with_chance(0.5)

    # Возможно это все достаточно неприлично.
    if dive and not operator:
        return "{}({})".format(choice_function(), gen_ft(depth - 1))  # Тут точно не нужны внешние скобки
    if not dive and operator:
        return ("({}(t) " + choice_operator() + " {})").format(choice_function(), gen_ft(depth - 1))
    if dive and operator:
        return ("({}({}) " + choice_operator() + " {})").format(choice_function(), gen_ft(depth - 1), gen_ft(depth - 1))
    if not operator and not dive:
        return "t"  # Тут точно не нужны внешние скобки


# Как то проверить функцию на предмет нечести.
def validate_function(f):
    try:
        return True
    except:
        return False


# Привести подобные слагаемые в f(t) (Хотя бы чуть-чуть).
def bring_similar(ft):
    ft = ft.replace("(t - t)", "(0)")
    ft = ft.replace("(t / t)", "(1)")
    ft = ft.replace("(t * t)", "(t ** 2)")
    ft = ft.replace("(t + t)", "(2 * t)")
    return ft


# Знак числа в строке (bruh)
def sign(number):
    if number < 0:
        return "- "
    return "+ "


# Генерирует строку, которая содержит диффур вида a1y' + a0y = f(t),
# при желании можно переделать под вид y' + a*y = b*f(t)
# Со скобками вроде все впорядке, но надо бы затестить на всякий пожарный
def gen_equation(a1_range, a0_range, precision, ft_depth, is_homogenous):
    a1 = set_precision(random.uniform(a1_range[0], a1_range[1]), precision)
    a0 = set_precision(random.uniform(a0_range[0], a0_range[1]), precision)

    # Чтобы не было лишних нулей
    if a1.is_integer():
        a1 = int(a1)
    if a0.is_integer():
        a0 = int(a0)

    if is_homogenous:
        ft = "0"
    else:
        ft = "t"
        while ft == "t":  # not validate_function(ft)
            ft = bring_similar(gen_ft(ft_depth))

    # Знак должен идти через пробел от числа, плюс в начале строки опускается
    return "{}{}y' {}{}y = {}".format(sign(a1).replace("+ ", ""), abs(a1), sign(a0), abs(a0), ft)
