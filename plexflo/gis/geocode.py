import pandas as pd
from geopy import Nominatim
import time

def latlon_search_in_dataframe(df, lat_colname, lon_colname, lat, lon, exact=False, match_radius=20):
    """
    Returns the row index of the dataframe that contains the lat/lon pair. Make sure that the lat/lon values are expressed in decimal degrees. Matching radius is in feet.
    :param df:
    :param lat_colname:
    :param lon_colname:
    :param lat:
    :param lon:
    :return:
    """
    if exact:
        lat_lon_df = df[df[lat_colname] == lat][df[lon_colname] == lon]
        # not empty data
        if len(lat_lon_df) > 0:
            return lat_lon_df
        else:
            return False
    else:
        lat_lon_df = df[(df[lat_colname] >= lat - match_radius/364000) & (df[lat_colname] <= lat + match_radius/364000)][(df[lon_colname] >= lon - match_radius/279840) & (df[lon_colname] <= lon + match_radius/279840)]
        # not empty data
        if len(lat_lon_df) > 0:
            return lat_lon_df[:1]
        else:
            return False

def address_to_latlon(C, address):
    time.sleep(1)
    geolocator = Nominatim(user_agent="third_party_82001")
    location = geolocator.geocode(address)
    return location.latitude, location.longitude

def latlon_to_address(C, lat, lon):
    time.sleep(1)
    locator = Nominatim(user_agent="myGeocoder")
    coordinates = f"{lat},{lon}"
    location = locator.reverse(coordinates)
    return location.display_name


# # create a dataframe with lat/lon values
# df = pd.DataFrame(columns=['lat', 'lon'])
# # fill random lat/lon values
# df['lat'] = pd.Series([42.819288])
# df['lon'] = pd.Series([-77.716442])
#
# print(df)
#
# x = latlon_search_in_dataframe(df, lat_colname='lat', lon_colname='lon', lat=42.819288, lon=-77.716442, exact=False, match_radius=20)
#
# print(x)