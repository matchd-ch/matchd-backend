
class BaseParamBuilder:

    def __init__(self, queryset, index):
        self.queryset = queryset
        self.index = index
        self.conditions = []

    def get_params(self):
        pass
