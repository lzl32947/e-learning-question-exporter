class CreateOutputError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f"CreateOutputError: {self.message}"


class OutputTypeError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f"OutputTypeError: {self.message}"