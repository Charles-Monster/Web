def greet():
    print("Hello!")


def welcome(func):
    print("Welcome!")
    func()


welcome(greet)
