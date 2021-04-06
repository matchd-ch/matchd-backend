
class BaseParamBuilder:

    def __init__(self, queryset, index):
        self.queryset = queryset
        self.index = index
        self.must = []
        self.should = []

    def get_params(self):
        pass
