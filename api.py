import requests
import logging
import pandas as pd

api_url = 'https://rickandmortyapi.com/api/location'
r = requests.get(api_url)
locations = r.json().get('results')


def get_locations(api_url=api_url):
    """
    Get locations from API
    :param api_url
    :return: locations list
    """
    r = requests.get(api_url)
    if r.status_code == 200:
        logging.info("SUCCESS")
        r = requests.get(api_url)
        locations = r.json().get('results')
        logging.info(f'len_locations = {len(locations)}')
        return locations
    else:
        logging.warning("HTTP STATUS {}".format(r.status_code))
        # raise AirflowException('Error in load page count')


def get_attributes_location(location):
    id_ = location['id']
    name = location['name']
    type_ = location['type']
    dimension = location['dimension']
    resident_cnt = len(location['residents'])
    return {
        'id': id_,
        'name': name,
        'type': type_,
        'dimenstion': dimension,
        'resident_cnt': resident_cnt
    }


def get_top_3_locations():
    locations_data = get_locations()
    locations = [get_attributes_location(location)
                 for location in locations_data]

    df = pd.DataFrame.from_records(locations)
    return df.sort_values('resident_cnt', ascending=False).iloc[:3]


if __name__ == '__main__':
    get_top_3_locations()
