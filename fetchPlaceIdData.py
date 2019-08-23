import fetchData
import json
import util

""" Fetches a list of place ids for further processing

Provide a geopoint, this script will fetch its nearby places
from Google, then generate a list of place ids for
fetchDistanceData.py to process.
"""


# loading environment variables
GOOGLE_API_KEY = util.GOOGLE_API_KEY
LAT = util.LATITUDE
LNG = util.LONGITUDE
PLACE_ID_FILE_PATH = util.PLACE_ID_FILE_PATH


# args validation
if GOOGLE_API_KEY == "":
    raise Exception("Google API key cannot be empty")
if LAT == "" or LNG == "":
    raise Exception("Latitude or longitude cannot be empty")
util.pathWritable(PLACE_ID_FILE_PATH)


def main():
    urls = formRequestUrls()
    fetchedData = fetchData.requestDataFromUrls(urls)
    jsonData = list(map(lambda data: json.loads(data), fetchedData))
    placeIdList = []
    for data in jsonData:
        placeIdList += [i["place_id"]
                        for i in data["results"] if i not in placeIdList]
    util.writeToPath("\n".join(placeIdList), PLACE_ID_FILE_PATH)


# place types are chosen to cover a wide range, so similiar types are not included.
# for avaliable types, see: https://developers.google.com/places/web-service/supported_types
placeTypes = ["aquarium", "art_gallery", "gym", 'library',
              'movie_theater', 'museum', 'park', 'restaurant', 'store', 'zoo']


def formRequestUrls():
    # form urls per defined placeTypes
    return list(map(lambda placeType: "https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={},{}&radius=50000&type={}&key={}".format(
        LAT, LNG, placeType, GOOGLE_API_KEY), placeTypes))


main()
