def decorator(func):
    def wrapper(name):
        print(" before the function.")
        func(name)
        print(" after the function.")

    return wrapper


@decorator
def greet(name):
    print(f"Hello, {name}!")


greet("Charles")
