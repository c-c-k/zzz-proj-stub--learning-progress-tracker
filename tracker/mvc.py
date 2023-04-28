import sys
from typing import Callable


class Singleton(type):
    _instances: dict = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(
                    Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class CommandHandler(metaclass=Singleton):
    def __init__(self):
        self._handlers = {}
        self.add_handler("", self._null_handler)

    def add_handler(self, code: str, handler: Callable):
        self._handlers[code] = handler

    def get_handler(self, code: str) -> Callable:
        return self._handlers.get(code, self._bad_input_handler)

    @staticmethod
    def _null_handler():
        print("No input")

    @staticmethod
    def _bad_input_handler():
        print("Unknown command!")


def register_handler(code):
    def _register(func):
        CommandHandler().add_handler(code, func)
        return func
    return _register


@register_handler(code="exit")
def exit_handler():
    print("Bye!")
    sys.exit(0)


def main():
    print("Learning Progress Tracker")
    command_handler = CommandHandler()

    while True:
        try:
            command_code = input().strip()
            command = command_handler.get_handler(command_code)
            command()
        except SystemExit:
            break


if __name__ == "__main__":
    main()
    pass
