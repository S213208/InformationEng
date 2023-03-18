import requests
from urllib.parse import urlencode


FIELDS = '{incidents{type,geometry{type,coordinates},properties{iconCategory}}}'
TOMTOM_API_KEY = "H90qT99QKgD0IzIadAPC7pIYsFkhY86L"


def get_traffic_data():
    url = f"https://api.tomtom.com/traffic/services/5/incidentDetails?key={TOMTOM_API_KEY}&bbox=1.08,52.01,1.22,52.10&fields={FIELDS}"
    #url = 'https://api.tomtom.com/traffic/services/5/incidentDetails?key={Your_Api_Key}&bbox={bbox}&fields={fields}&language={language}&t={t}&categoryFilter={categoryFilter}&timeValidityFilter={timeValidityFilter}'
    #https://{baseURL}/traffic/services/{versionNumber}/incidentDetails?key={Your_Api_Key}&ids={ids}&fields={fields}&language={language}&t={t}&categoryFilter={categoryFilter}&timeValidityFilter={timeValidityFilter}
    response = requests.get(url)
    data = response.json()
    print(data)

get_traffic_data()