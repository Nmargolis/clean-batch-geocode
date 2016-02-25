import mapbox
import os
import pprint

# pp = pprint.PrettyPrinter(indent=4)

mapbox_token = os.environ['MAPBOX_TOKEN']
geocoder = mapbox.Geocoder(access_token=mapbox_token)


# TODO: Decide whether defaults should be 0 or center of Oakland
def geocode_address(address, proxim_lat=37.8044, proxim_lon=-122.2697):
    """Takes an address string and optional lat and lon for proximity and returns dictionary of place_name, relevance, lat and lon if successful

        >>> sorted(geocode_address('3425 Foxtail Terrace, Fremont, CA').items())
        [('lat', 37.561203), ('lon', -122.003467), ('place_name', u'3425 Foxtail Ter, Fremont, California 94536, United States'), ('relevance', 0.996)]')
    """

    response_dict = {}

    response = geocoder.forward(address, lon=proxim_lon, lat=proxim_lat)

    response = response.geojson()

    if response['features']:
        response_dict['place_name'] = response['features'][0]['place_name']
        response_dict['relevance'] = response['features'][0]['relevance']
        response_dict['lon'], response_dict['lat'] = response['features'][0]['center']

    # print response_dict

    return response_dict
