import equation_generator
from some_stuff import *

if __name__ == '__main__':
    chance_homogenous = 0.03
    chance_separable = 0.50
    ft_max_depth = 2

    a1_range = (-10, 10)
    a0_range = (-20, -10)
    precision = 2

    with open("tests.txt", 'w') as ost:
        for i in range(0, 100):
            equation = equation_generator.gen_equation(a1_range, a0_range, precision, ft_max_depth,
                                                       true_with_chance(chance_homogenous),
                                                       true_with_chance(chance_separable))
            ost.write(equation[:] + '\n')
