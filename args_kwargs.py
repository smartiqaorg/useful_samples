

"""
Example 1. Count items in bag
"""


# Counts arguments quantity
def count_items_in_bag(*args):
    sum = 0
    for item in args:
        print(f'Counting {item}')
        sum += 1
    print(f'Total items: {sum}')
    return


def count_named_items_in_fridge(**kwargs):
    sum = 0
    for name, quantity in kwargs.items():
        print(f'Counting {name}={quantity}')
        sum += quantity
    print(f'Total items: {sum}')
    return


print('#  ==  Example 1  ==')
count_items_in_bag('phone', 'credit card', 'pen', 'notebook', 'handkerchief')
count_named_items_in_fridge(milk=1, apple=5, eggs=10, butter=1)


"""
Example 2. Use positional params in different order
"""


def print_args(a, b=0, **kwargs):
    print("\nLets print args:")
    print(f'a={a}')
    print(f'b={b}')
    for key, value in kwargs.items():
        print(f'{key}={value}')


print('\n#  ==  Example 2  ==')
# The first 2 args could be unnamed since they are passed in the initial order
print_args(1, 2, named_arg=100, one_more_named_arg="I'm one more named arg!")
# We can change args order - but we need to specify their names in such case
print_args(named_arg=100, b=2, a=1, one_more_named_arg="I'm one more named arg!")
# We can skip 'b' param value since it already has default one (b=0)
print_args(named_arg=100, a=1, one_more_named_arg="I'm one more named arg!")


"""
Example 3. Use positional params in different order
"""


def print_func_name_and_call(times, func, *args):
    for iteration in range(0, times):
        print(f'Function name is "{func.__name__}" ({iteration})')
    return func(*args)


def sum(*args):
    sum = 0
    for item in args:
        sum += item
    return sum


print('\n#  ==  Example 3  ==')
# Here we pass sum() function name and its arguments 10, 100, 1000
s = print_func_name_and_call(3, sum, 10, 100, 1000)
print(f'Sum is {s}')