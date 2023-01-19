import sympy as smp
import concurrent.futures


def grad_error(y_disk, y_part, diff_a_part, diff_b_part):
    error, grad_a, grad_b = 0, 0, 0
    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = [executor.submit(compute_deltas, point, y_part, diff_a_part, diff_b_part) for point in y_disk]
        for future in concurrent.futures.as_completed(results):
            delta_y, delta_grad_a, delta_grad_b = future.result()
            grad_a -= delta_grad_a
            grad_b -= delta_grad_b
            error += delta_y ** 2
    return 0.5 * error, grad_a, grad_b


def compute_deltas(point, y_part, diff_a_part, diff_b_part):
    delta_y = (point[1] - y_part.subs('t', point[0]))
    delta_grad_a = delta_y * diff_a_part.subs('t', point[0])
    delta_grad_b = delta_y * diff_b_part.subs('t', point[0])
    return delta_y, delta_grad_a, delta_grad_b


if __name__ == '__main__':
    test_file_name = "tests/test8.test"
    with open(test_file_name, 'r') as ist:
        a, b, t, c = smp.Symbol('a'), smp.Symbol('b'), smp.Symbol('t'), smp.Symbol('c')

        ft = smp.parsing.sympy_parser.parse_expr(ist.readline())
        points_size = int(ist.readline())

        # Истинное и предсказанное решение (неопределенное)
        y_disc = [tuple([float(value) for value in ist.readline().split()]) for point in range(points_size)]
        y_gen = b * smp.exp(a * t) * (smp.integrate(ft / (smp.exp((a * t))), t) + c)

        # Частные производные в общем виде
        diff_a_gen = smp.diff(y_gen, 'a')
        diff_b_gen = smp.diff(y_gen, 'b')

        # Инициализируем параметры метода Adam
        beta1 = 0.9
        beta2 = 0.999
        epsilon = 1e-8

        # Начальное значение a и b
        a_, b_ = -5, -5
        # Начальное значение веса
        learning_rate = 0.01

        # инициализируем нулевые значения для m и v
        m_a, m_b = 0.0, 0.0
        v_a, v_b = 0.0, 0.0

        iteration = 0
        error = 1
        while error > 1e-12:
            iteration += 1

            # c - Задача Коши для первой точки
            abc = {'a': a_,
                   'b': b_,
                   'c': smp.solve(y_gen.subs({'t': y_disc[1][0], 'a': a_, 'b': b_}) - y_disc[1][1], c)[0]}
            # Вычисляем ошибку и градиент одновременно (оптимизация)
            error, grad_a, grad_b = grad_error(y_disc,
                                               y_gen.subs(abc),
                                               diff_a_gen.subs(abc),
                                               diff_b_gen.subs(abc))

            # Выводим текущее значение функции ошибки
            print(f"Iteration: {iteration}, Error: {error}, a:{a_}, b:{b_}")

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
            a_ -= learning_rate * m_a_corr / (smp.sqrt(v_a_corr) + epsilon)
            b_ -= learning_rate * m_b_corr / (smp.sqrt(v_b_corr) + epsilon)
