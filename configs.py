import os
import sympy

configs = [
    {
        "count": 10,
        "depth": 1,
        "t0": 10,
        "tn": 20,
        "points": 11,
        "a_range": (-10, -1),
        "b_range": (-10, -1),
        "max_value": 10 ** 6,
        "tests_path": "tests",
        "answers_path": os.path.join("tests", "answers"),
        "separable": False,
        "homogenous": False,
        "distribution": "random"
    }
]