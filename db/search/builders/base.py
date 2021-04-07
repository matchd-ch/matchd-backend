from dateutil.relativedelta import relativedelta


class BaseParamBuilder:

    def __init__(self, queryset, index):
        self.queryset = queryset
        self.index = index
        self.must_conditions = []
        self.should_conditions = []
        self.filter_conditions = []
        self.must_not_conditions = []

    def get_params(self):
        pass

    def get_condition(self, path, prop, value, boost=1, condition_type='bool'):
        return {
            'nested': {
                'path': path,
                'query': {
                    condition_type: {
                        'must': {
                            'terms': {
                                f'{path}.{prop}': value
                            },
                        }
                    }
                },
                'boost': boost
            },
        }

    def get_range_query(self, key, date_from, date_to, months, boost):
        shifted_start = self.get_shifted_date(date_from, -months)
        shifted_end = self.get_shifted_date(date_to, +months)
        return {
            # boost dates within the shifted range
            "range": {
                key: {
                    "gte": shifted_start.strftime('%Y-%m-%d'),
                    "lte": shifted_end.strftime('%Y-%m-%d'),
                    "boost": boost
                }
            }
        }

    def get_shifted_date(self, date, months):
        return date + relativedelta(months=months)
