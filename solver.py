import sympy as smp
import matplotlib.pyplot as plt
import numpy as np


def calc_err(y_disk, y_particular):
    # print(y_particular)
    error = 0
    for point in y_disk:
        error += (point[1] - y_particular.subs('t', point[0])) ** 2
    return 0.5 * error


def calc_grad(y_disk, y_particular, a, b):
    grad_a, grad_b = 0, 0
    diff_a = smp.diff(y_particular, 'a').subs({'a': a, 'b': b})
    diff_b = smp.diff(y_particular, 'b').subs({'a': a, 'b': b})
    y_particular = y_particular.subs({'a': a, 'b': b})
    for point in y_disk:
        grad_a -= (point[1] - y_particular.subs('t', point[0])) * diff_a.subs('t', point[0])
    for point in y_disk:
        grad_b -= (point[1] - y_particular.subs('t', point[0])) * diff_b.subs('t', point[0])
    return tuple([grad_a, grad_b])


# print(y_disc[1][0], y_disc[1][1])  # Первая точка
# print(y_disc[1][0], y_particular.subs(params))  # Первая точка частного решения
def err(a_, b_):
    a = smp.Symbol('a')
    b = smp.Symbol('b')
    t = smp.Symbol('t')
    c = smp.Symbol('c')
    y_general = b * smp.exp(a * t) * (smp.integrate(ft / (smp.exp((a * t))), t) + c)  # Общее решение

    params = {'t': y_disc[1][0],
              'a': a_,
              'b': b_}
    c = smp.solve(y_general.subs(params) - y_disc[1][1], c)[0]  # Задача Коши
    y_particular = y_general.subs('c', c)  # Частное решение
    error = calc_err(y_disc, y_particular.subs({'a': params['a'], 'b': params['b']}))
    return error


def grad(a_, b_):
    a = smp.Symbol('a')
    b = smp.Symbol('b')
    t = smp.Symbol('t')
    c = smp.Symbol('c')
    y_general = b * smp.exp(a * t) * (smp.integrate(ft / (smp.exp((a * t))), t) + c)  # Общее решение

    params = {'t': y_disc[1][0],
              'a': a_,
              'b': b_}
    c = smp.solve(y_general.subs(params) - y_disc[1][1], c)[0]  # Задача Коши
    y_particular = y_general.subs('c', c)  # Частное решение
    return calc_grad(y_disc, y_particular, params['a'], params['b'])


def paint_err():
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1, projection='3d')

    true_a = 2
    true_b = 3
    delta_a = 0.1
    delta_b = 0.1
    points = 5
    a_space = np.linspace(true_a - delta_a, true_a + delta_a, points)
    np.delete(a_space, 0)
    b_space = np.linspace(true_b - delta_b, true_b + delta_b, points)
    np.delete(b_space, 0)
    x, y = np.meshgrid(a_space, b_space)
    z = np.array([[err(a, b) for a in a_space] for b in b_space])
    ax.plot_surface(x, y, z)
    ax.set_xlabel('a')
    ax.set_ylabel('b')
    ax.set_zlabel('error')
    plt.show()


if __name__ == '__main__':
    test_file_name = "simple_test.test"
    with open(test_file_name, 'r') as ist:
        ft = smp.parsing.sympy_parser.parse_expr(ist.readline())
        n = int(ist.readline())
        y_disc = [tuple([float(i) for i in ist.readline().split()]) for j in range(n)]
        # paint_err()
        # Начальное значение a и b
        a, b = -10, 25
        # Начальное значение веса
        learning_rate = 0.01
        # Количество итераций
        num_iterations = 1000

        for i in range(num_iterations):
            # Вычисляем градиент
            grad_a, grad_b = grad(a, b)
            print(grad_a, grad_b)
            # Обновляем веса
            a -= learning_rate * grad_a
            b -= learning_rate * grad_b
            # Выводим текущее значение функции ошибки
            print("Iteration: {}, Error: {}, a:{}, b:{}".format(i, err(a, b), a, b))
