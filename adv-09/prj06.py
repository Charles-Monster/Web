class Repeat:
    def times(self, n):
        def decorator(func):
            def wrapper(*args, **kwargs):
                for _ in range(n):
                    result = func(*args, **kwargs)
                return result

            return wrapper

        return decorator


repeat = Repeat()


@repeat.times(4)
def say_hello(name):
    print(f"Hello, {name}!")


say_hello("Charles")
