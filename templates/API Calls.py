import requests
from urllib.parse import urlencode
import datetime

TOMTOM_API_KEY = "H90qT99QKgD0IzIadAPC7pIYsFkhY86L"
VISUAL_CROSSING_API_KEY = 'LZCZ4VPZ4NJZKZPCDZGYR8GA7'

#TOM TOM calls
FIELDS = '{incidents{type,geometry{type,coordinates},properties{iconCategory}}}'

# Ipswich coordinates
latitude = 52.056736
longitude = 1.148220

# Calculate the date range for the past year
today = datetime.date.today()
last_year = today - datetime.timedelta(days=365)

# Format dates for the API request
start_date = last_year.strftime('%Y-%m-%d')
end_date = today.strftime('%Y-%m-%d')


def get_traffic_data():
    url = f"https://api.tomtom.com/traffic/services/5/incidentDetails?key={TOMTOM_API_KEY}&bbox=1.08,52.01,1.22,52.10&fields={FIELDS}"
    response = requests.get(url)
    data = response.json()
    print(data)


def get_weather_data():
    url = f'https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/weatherdata/history?&aggregateHours=24&startDateTime={start_date}&endDateTime={end_date}&unitGroup=uk&contentType=json&dayStartTime=0:0:00&dayEndTime=0:0:00&location=Ipswich,UK&key={VISUAL_CROSSING_API_KEY}'
    response = requests.get(url)
    print(response)
    weather_data = response.json()
    print(weather_data)

# Process the weather_data as needed

get_traffic_data()
get_weather_data()