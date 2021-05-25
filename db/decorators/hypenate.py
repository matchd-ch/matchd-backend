import pyphen


def hyphenate(func):
    def hypenate_word(dic, word):
        return dic.inserted(word, hyphen='\u00AD')

    def get_attribute_from_function(function):
        return function.__name__.replace('resolve_', '').replace('display_', '')

    def wrapper(self, obj):
        attribute = get_attribute_from_function(func)
        value = func(self, obj)

        if value is None:
            return value

        # determine language for current value
        value = getattr(self, attribute)
        dic = pyphen.Pyphen(lang='de-De')
        hyphenated = []
        words = value.split(' ')
        for word in words:
            if '-' in word:  # attention: this is a en dash!
                hyphenated.append('-'.join([hypenate_word(dic, w) for w in word.split('-')]))
            elif '–' in word:  # attention: this is a em dash!
                hyphenated.append('–'.join([hypenate_word(dic, w) for w in word.split('–')]))
            elif len(word) > 4:
                hyphenated.append(hypenate_word(dic, word))
            else:
                hyphenated.append(word)
        return ' '.join(hyphenated)
    return wrapper
