from dateutil.relativedelta import relativedelta


# pylint: disable=R0913
class BaseParamBuilder:

    def __init__(self, queryset, index, first, skip):
        self.queryset = queryset
        self.index = index
        self.first = first
        self.skip = skip
        self.must_conditions = []
        self.should_conditions = []
        self.filter_conditions = []

    def get_params(self):
        pass

    def get_condition(self, path, prop, value, boost=1, condition_type='bool'):
        return {
            'nested': {
                'path': path,
                'query': {
                    condition_type: {
                        'should': [
                            {
                                'terms': {
                                    f'{path}.{prop}': value
                                }
                            }
                        ]
                    }
                },
                'boost': boost
            },
        }

    def get_range_query(self, key, value, shift, boost):
        shifted_start = value - shift
        shifted_end = value + shift
        shifted_start = max(0, shifted_start)
        shifted_end = min(100, shifted_end)
        return {
            # boost dates within the shifted range
            "range": {
                key: {
                    "gte": shifted_start,
                    "lte": shifted_end,
                    "boost": boost
                }
            }
        }

    def get_date_range_query(self, key, date_from, date_to, months, boost):
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

    def get_nested_date_range_query(self, from_key, to_key, date_from, date_to, months, boost):
        shifted_start = self.get_shifted_date(date_from, -months)
        shifted_end = self.get_shifted_date(date_to, +months)
        return {
            'bool': {
                'should': [
                    {
                        # boost start date within range
                        "range": {
                            from_key: {
                                "gte": shifted_start.strftime('%Y-%m-%d'),
                                "lte": shifted_end.strftime('%Y-%m-%d'),
                                "boost": boost
                            }
                        }
                    },
                    {
                        # boost end date within range
                        "range": {
                            to_key: {
                                "gte": shifted_start.strftime('%Y-%m-%d'),
                                "lte": shifted_end.strftime('%Y-%m-%d'),
                                "boost": boost
                            }
                        }
                    }
                ]
            }
        }

    def get_shifted_date(self, date, months):
        return date + relativedelta(months=months)
