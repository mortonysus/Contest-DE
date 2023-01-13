import random

functions = [
    "sin",
    "cos",
    "tg",
    "sqrt",
    "exp",
    "ln"
]

operators = ["+", "-", "*", "/"]


# Генерирует строку, которая содержит "случайное" математическое выражение, зависящее от t.
# Чтобы увеличить веселость выражения на выходе - нужно поднять depth
# Можно обмазаться скобками при желании
# Пока возникают перлы в виде ln(t - t) итд,
# можно попытаться от них избавиться или проверть выражение на валидность в другом месте
# можно добавить чиселок, но суть не в чиселках
def gen_ft(depth):
    # Выбираем:
    #   Оператор и еще одно выражение
    #   Увеличить вложенность
    #   Оператор и увеличить
    #   Ничего не делать

    # Теоретически это даст возможность получить любые комбинации выражений с глубиной вложенности не больше заданной
    if depth == 0:
        return "t"

    dive = random.randint(0, 1)
    mul = random.randint(0, 1)
    func = random.choice(functions)

    if dive and not mul:
        return "{}({})".format(func, gen_ft(depth - 1))
    if not dive and mul:
        return ("{}(t) " + random.choice(operators) + " {}").format(func, gen_ft(depth - 1))
    if dive and mul:
        return ("{}({} " + random.choice(operators) + " {})").format(func, gen_ft(depth - 1), gen_ft(depth - 1))
    if not mul and not dive:
        return "t"


# Обрезать лишние знаки у десятичного представления числа.
def cut_exponent(float_number, precision):
    return float("%.{}f".format(precision) % float_number)


# Знак числа в строке (bruh)
def sign(number):
    if number < 0:
        return "- "
    return "+ "


# Генерирует строку, которая содержит диффур вида a1y' + a0y = f(t),
# при желании можно переделать под вид y' + a*y = b*f(t)
# Скобок больше чем нужно, но не меньше, например
def gen_equation(a1_range, a0_range, precision, ft_depth):
    a1 = cut_exponent(random.uniform(a1_range[0], a1_range[1]), precision)
    a0 = cut_exponent(random.uniform(a0_range[0], a0_range[1]), precision)

    # Чтобы не было лишних нулей
    if a1.is_integer():
        a1 = int(a1)
    if a0.is_integer():
        a0 = int(a0)

    ft = gen_ft(ft_depth)
    # Знак должен идти через пробел от числа, плюс в начале строки опускается
    return "{}{}y' {}{}y = {}".format(sign(a1).replace("+ ", ""), abs(a1), sign(a0), abs(a0), ft)
