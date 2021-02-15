
class FormException(Exception):

    def __init__(self, errors):
        self.errors = errors
        super().__init__()


class NicknameException(FormException):

    def __init__(self, errors, suggestions):
        self.suggestions = suggestions
        super().__init__(errors)
