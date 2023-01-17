import sympy as smp

if __name__ == '__main__':
    test_file_name = "simple_test.test"
    with open(test_file_name, 'r') as ist:
        ft = smp.parsing.sympy_parser.parse_expr(ist.readline())
        n = int(ist.readline())
        y = [tuple([float(i) for i in ist.readline().split()]) for j in range(n)]
