import sympy as smp
import matplotlib.pyplot as plt
import numpy as np
import math


def calc_err(y_disk, y_particular):
    return 0.5 * sum([(point[1] - y_particular.subs('t', point[0])) ** 2 for point in y_disk])


def calc_grad(y_disk, y_particular, a, b):
    grad_a, grad_b = 0, 0
    diff_a = smp.diff(y_particular, 'a').subs({'a': a, 'b': b})
    diff_b = smp.diff(y_particular, 'b').subs({'a': a, 'b': b})
    y_particular = y_particular.subs({'a': a, 'b': b})
    for point in y_disk:
        grad_a -= (point[1] - y_particular.subs('t', point[0])) * diff_a.subs('t', point[0])
        grad_b -= (point[1] - y_particular.subs('t', point[0])) * diff_b.subs('t', point[0])
    return grad_a, grad_b


def error(a_, b_, y_gen):
    a, b, t, c = smp.Symbol('a'), smp.Symbol('b'), smp.Symbol('t'), smp.Symbol('c')

    params = {'t': y_disc[1][0],
              'a': a_,
              'b': b_}
    c = smp.solve(y_gen.subs(params) - y_disc[1][1], c)[0]  # Задача Коши
    return calc_err(y_disc, y_gen.subs({'a': params['a'], 'b': params['b'], 'c': c}))


def grad(a_, b_, y_gen):
    a, b, t, c = smp.Symbol('a'), smp.Symbol('b'), smp.Symbol('t'), smp.Symbol('c')

    params = {'t': y_disc[1][0],
              'a': a_,
              'b': b_}
    c = smp.solve(y_gen.subs(params) - y_disc[1][1], c)[0]  # Задача Коши
    y_particular = y_gen.subs('c', c)  # Частное решение
    return calc_grad(y_disc, y_particular, params['a'], params['b'])


def paint_err(y_gen):
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1, projection='3d')

    true_a = -2
    true_b = 3
    delta_a = 10
    delta_b = 10
    points = 5
    a_space = np.linspace(true_a - delta_a, true_a + delta_a, points)
    np.delete(a_space, 0)
    b_space = np.linspace(true_b - delta_b, true_b + delta_b, points)
    np.delete(b_space, 0)
    x, y = np.meshgrid(a_space, b_space)
    z = np.array([[error(a, b, y_gen) for a in a_space] for b in b_space])
    ax.plot_surface(x, y, z)
    ax.set_xlabel('a')
    ax.set_ylabel('b')
    ax.set_zlabel('error')
    plt.show()


if __name__ == '__main__':
    test_file_name = "simple_test.test"
    with open(test_file_name, 'r') as ist:
        ft = smp.parsing.sympy_parser.parse_expr(ist.readline())
        points_size = int(ist.readline())
        y_disc = [tuple([float(value) for value in ist.readline().split()]) for point in range(points_size)]

        # Инициализируем параметры метода Adam
        beta1 = 0.9
        beta2 = 0.999
        epsilon = 1e-8

        # Начальное значение a и b
        a_, b_ = -10, 25
        # Начальное значение веса
        learning_rate = 0.1

        # инициализируем нулевые значения для m и v
        m_a, m_b = 0, 0
        v_a, v_b = 0, 0

        iteration = 0
        while True:
            iteration += 1
            a, b, t, c = smp.Symbol('a'), smp.Symbol('b'), smp.Symbol('t'), smp.Symbol('c')
            y_gen = b * smp.exp(a * t) * (smp.integrate(ft / (smp.exp((a * t))), t) + c)  # Общее решение

            # Выводим текущее значение функции ошибки
            err = error(a_, b_, y_gen)
            print(f"Iteration: {iteration}, Error: {err}, a:{a_}, b:{b_}")
            if err < 0.001:
                break

            # Вычисляем градиент
            grad_a, grad_b = grad(a_, b_, y_gen)

            # Обновляем значения для m и v
            m_a = beta1 * m_a + (1 - beta1) * grad_a
            m_b = beta1 * m_b + (1 - beta1) * grad_b
            v_a = beta2 * v_a + (1 - beta2) * grad_a ** 2
            v_b = beta2 * v_b + (1 - beta2) * grad_b ** 2

            # Вычисляем корректировку bias
            m_a_corr = m_a / (1 - beta1)
            m_b_corr = m_b / (1 - beta1)
            # Вычисляем корректировку bias
            v_a_corr = v_a / (1 - beta2)
            v_b_corr = v_b / (1 - beta2)

            # Обновляем веса
            a_ -= learning_rate * m_a_corr / (math.sqrt(v_a_corr) + epsilon)
            b_ -= learning_rate * m_b_corr / (math.sqrt(v_b_corr) + epsilon)
