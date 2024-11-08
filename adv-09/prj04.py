def decorator(func):
    def wrapper(*args, **kwargs):
        print("something before the function.")
        result = func(*args, **kwargs)
        print("something after the function.")
        return result

    return wrapper


@decorator
def greet(name=None):
    if name:
        print(f"Hello, {name}!")
    else:
        print("Hello!")


greet()


greet("Charles")
