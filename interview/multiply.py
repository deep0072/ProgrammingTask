from functools import reduce


def multiply(ls):
    mul = reduce(lambda x, y: x * y, ls)
    return mul


ans = multiply((1, 2, 3))
print(ans)
