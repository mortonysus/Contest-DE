import os
import sympy

configs = [
    {
        "count": 2,
        "depth": 1,
        "t0": 10,
        "tn": 20,
        "points": 11,
        "a_range": (1, 1),
        "b_range": (1, 1),
        "max_value": 10 ** 12,
        "tests_path": "tests",
        "answers_path": os.path.join("tests", "answers"),
        "separable": False,
        "homogenous": False,
        "distribution": "random",
        "timeout" : 5
    }
]