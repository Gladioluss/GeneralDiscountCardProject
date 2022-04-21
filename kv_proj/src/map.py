from googlemaps import Client
from pprint import pprint
import requests
import dgis



DGIS_MAPS_APIKEY = 'ruyula3447'
ADDRESS = 'Екатеринбург, Ленина, 54'
URL = 'https://catalog.api.2gis.com/3.0/items/geocode?'


def Main():
    response = requests.get(f'{URL}q={ADDRESS}&fields=items.point&key={DGIS_MAPS_APIKEY}')
    print(response.json())
    lat = 55.751508
    lon = 37.615666
    response = requests.get(f'https://catalog.api.2gis.com/3.0/items/geocode?lat={lat}&lon={lon}&fields=items.point&key={DGIS_MAPS_APIKEY}')
    print(response.json())





if __name__ == '__main__':
    Main()






# map_client = Client(DGIS_MAPS_APIKEY)
# pprint(map_client.geocode('ул. Малышева, 32, Екатеринбург, Свердловская обл.'))