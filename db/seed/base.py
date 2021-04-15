from db.seed import Random


class BaseSeed:

    def __init__(self):
        self.rand = Random()

    def create_or_update(self, data, *args, **kwargs):
        raise NotImplementedError()

    def random(self, *args, **kwargs):
        raise NotImplementedError()
