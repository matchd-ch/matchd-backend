from api.data import zip_city_datasource


def filter_correct_zip_and_city(zip_mapping: dict[str:str]):
    # assume the following job posting zip values
    # zip_mapping = {'9000': 'St. Gallen', '9470': 'Buchs SG'}
    #
    # if we only match the zip value we will end up with the following list, which is not correct:
    # [{
    #     "zip": "9000",
    #     "city": "St. Gallen",
    #     "canton": "SG"
    # },
    # {
    #     "zip": "9470",
    #     "city": "Buchs SG",
    #     "canton": "SG"
    # },
    # {
    #     "zip": "9470",
    #     "city": "Werdenberg",  # should not be in the result
    #     "canton": "SG"
    # }]
    #
    # to avoid this, we so also check the canton value

    result = []

    for obj in zip_city_datasource.data:
        data_zip = str(obj.get('zip'))
        if data_zip in zip_mapping:
            city_canton = zip_mapping[data_zip].split(' ')
            city_value = city_canton[0]
            canton_value = ''
            if len(city_canton) > 1:
                canton_value = city_canton[-1]
            data_canton = obj.get('canton')
            if canton_value == data_canton:
                if city_value == obj.get('city').split(f' {data_canton}')[0]:
                    result.append(obj)
            else:
                if zip_mapping[data_zip] == obj.get('city'):
                    result.append(obj)

    return result
