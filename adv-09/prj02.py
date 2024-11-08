def decorator(func):
    def wrapper():
        print("something before the function.")
        func()
        print("something after the function.")

    return wrapper


@decorator
def greet():
    print("Hello!")


greet()
