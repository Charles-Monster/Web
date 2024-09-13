add_ten = lambda x: x + 10
print(add_ten(5))


def my_func(n):
    return lambda x: x * n


dobule_num = my_func(2)
triple_num = my_func(3)
print(dobule_num(5))
print(triple_num(5))
