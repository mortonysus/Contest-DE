import sympy as smp


def Err(y_disk, y):
    return 0.5 * sum([(point[1] - y.subs('t', point[0])) ** 2 for point in y_disk])


if __name__ == '__main__':
    test_file_name = "simple_test.test"
    with open(test_file_name, 'r') as ist:
        ft = smp.parsing.sympy_parser.parse_expr(ist.readline())
        n = int(ist.readline())
        y_disc = [tuple([float(i) for i in ist.readline().split()]) for j in range(n)]

        a = smp.Rational(1)
        b = smp.Rational(3)
        t = smp.Symbol('t')
        c = smp.Symbol('c')

        sub_int_func = ft / (smp.exp((a * t)))
        ind_int = smp.integrate(sub_int_func, t)
        y = b * smp.exp(a * t) * (ind_int + c)
        c = smp.solve(y.subs('t', y_disc[1][0]) - y_disc[1][1], c)[0]
        y = y.subs('c', c)

        print(y_disc[1][0], y_disc[1][1])
        print(y_disc[1][0], y.subs({'t': y_disc[1][0]}))
        print(Err(y_disc, y))
