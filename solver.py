import sympy as smp


def err(y_disk, y_particular):
    error = 0
    for point in y_disk:
        error += (point[1] - y_particular.subs('t', point[0])) ** 2
    return 0.5 * error


def grad_err(y_disk, y_particular, a, b):
    grad_a, grad_b = 0, 0
    diff_a = smp.diff(y_particular, 'a').subs({'a': a, 'b': b})
    diff_b = smp.diff(y_particular, 'b').subs({'a': a, 'b': b})
    y_particular = y_particular.subs({'a': a, 'b': b})
    for point in y_disk:
        grad_a -= (point[1] - y_particular.subs('t', point[0])) * diff_a.subs('t', point[0])
    for point in y_disk:
        grad_b -= (point[1] - y_particular.subs('t', point[0])) * diff_b.subs('t', point[0])
    return tuple([grad_a, grad_b])


if __name__ == '__main__':
    test_file_name = "simple_test.test"
    with open(test_file_name, 'r') as ist:
        ft = smp.parsing.sympy_parser.parse_expr(ist.readline())
        n = int(ist.readline())
        a = smp.Symbol('a')
        b = smp.Symbol('b')
        t = smp.Symbol('t')
        c = smp.Symbol('c')
        y_disc = [tuple([float(i) for i in ist.readline().split()]) for j in range(n)]
        y_general = b * smp.exp(a * t) * (smp.integrate(ft / (smp.exp((a * t))), t) + c)  # Общее решение

        params = {'t': y_disc[1][0],
                  'a': 2.000000001,
                  'b': 3}
        c = smp.solve(y_general.subs(params) - y_disc[1][1], c)[0]  # Задача Коши
        y_particular = y_general.subs('c', c)  # Частное решение
        print(y_disc[1][0], y_disc[1][1])  # Первая точка
        print(y_disc[1][0], y_particular.subs(params))  # Первая точка частного решения
        print(err(y_disc, y_particular.subs({'a': params['a'], 'b': params['b']})))  # Ошибка частного решения
        print(grad_err(y_disc, y_particular, params['a'], params['b']))  # Градиент функции ошибки
