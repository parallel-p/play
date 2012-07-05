import functools
import operator
def factorial(n):
    return functools.reduce(operator.mul, range(1, n + 1), 1)

print(factorial(10))
