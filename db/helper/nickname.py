from django.core.exceptions import ValidationError

from db.validators import NicknameValidator


# noinspection PyBroadException
class NicknameHelper:

    def validate(self, user, nickname):
        validator = NicknameValidator()
        validator.validate(user, nickname)

    def get_suggestions(self, user, nickname):
        patterns = [
            '***iii',
            '***.iii',
            'fn.ln',
            'fn.lniii',
            'fn.ln.iii',
        ]
        validator = NicknameValidator()
        suggestions = []
        i = 1
        while len(suggestions) < 5:
            for pattern in patterns:
                try:
                    suggestion = pattern\
                        .replace('***', nickname)\
                        .replace('iii', str(i))\
                        .replace('fn', user.first_name)\
                        .replace('ln', user.last_name)
                    validator.validate(user, pattern)
                    suggestions.append(suggestion.lower())
                except ValidationError:
                    pass
            i += 1

        return suggestions
