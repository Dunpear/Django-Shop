import requests
import json
from verkana_front.settings import BASE_URL




def send(url, method, data=None, headers=None):
    if headers is None:
        result = requests.request(method, BASE_URL + url, json=data).text
        get_data = json.loads(result)
        return get_data
    else:
        result = requests.request(method, BASE_URL + url, json=data, headers=headers).text
        get_data = json.loads(result)
        return get_data




def delete(url, headers=None):

    result = requests.delete(BASE_URL + url, headers=headers)
    print(result)
    # get_data = json.loads(result)
    return result