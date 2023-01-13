import equation_generator
import numpy


# Вернет true с переданной вероятностью [0:1]
def chance_condition(chance):
    return numpy.random.choice([True, False], p=[chance, 1 - chance])


if __name__ == '__main__':
    chance_homogenous = 0.03
    is_homogenous = chance_condition(chance_homogenous)
    ft_max_depth = 2

    a1_range = (-10, 10)
    a0_range = (-20, -10)
    precision = 2

    print(equation_generator.gen_equation(a1_range, a0_range, precision, ft_max_depth, is_homogenous))
