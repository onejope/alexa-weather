import requests
from datetime import datetime, timedelta, timezone
import urllib.parse

NWS_API_BASE_URL = 'https://api.weather.gov/'

DEFAULT_USER_AGENT = 'nws-alexa-weather-notification'
DEFAULT_HEADERS = {'user-agent': DEFAULT_USER_AGENT}

#TODO
def get_grid_points(coordinates: str):
    points_url = '{NWS_API_BASE_URL}points/{coordinates}'
    print(points_url)

    #points = requests.get(points_url)
    #print(points.status_code)
    #print(points.text)


def get_weather_station_urls(coordinates: str):
    find_station_url = '{}points/{}/stations'.format(NWS_API_BASE_URL, coordinates)

    headers = {'user-agent': DEFAULT_USER_AGENT}

    stations_data = requests.get(find_station_url, headers=DEFAULT_HEADERS).json()
    return stations_data['observationStations']

def get_latest_temperature_in_c_from_station(station_urls: [str]):
    for station_url in station_urls:
        stations_observations_url = '{}/observations'.format(station_url)
        current_time = datetime.now(timezone.utc)
        start_time = current_time - timedelta(hours=1)
        params = {'start': start_time.strftime("%Y-%m-%dT%H:%M:%S%z"), 'end': current_time.strftime("%Y-%m-%dT%H:%M:%S%z"), 'limit': 2}

        observations = requests.get(stations_observations_url, headers=DEFAULT_HEADERS, params=params).json()
        
        for observation in observations['features']:
            if observation['properties']['temperature']['value']:
                print('Found temperature from following URL: %s' % station_url)
                return observation['properties']['temperature']['value']
        
        print('No observations found for station URL: %s' % station_url)

    # No observations with valid temperature was found.
    print('No observations found')
    return None

def get_latest_temperature_in_c_for_coordinates(coordinates: str):
    weather_station_urls = get_weather_station_urls(coordinates=coordinates)
    return get_latest_temperature_in_c_from_station(weather_station_urls)
