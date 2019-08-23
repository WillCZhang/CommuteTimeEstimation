import fetchData
import json
import util

""" Fetches travel info from Google for further processing

This script takes in a place id list, generates a list of
unique combination of two place ids, then fetches travel
info (e.g. distance, time, etc.) of each two places
combination from Google. Avaliable travel modes:
"driving", "walking", "bicycling", "transit"
"""


# loading environment variables
GOOGLE_API_KEY = util.GOOGLE_API_KEY
PLACE_ID_FILE_PATH = util.PLACE_ID_FILE_PATH
DISTANCE_DATA_FILE_PATH = util.DISTANCE_DATA_FILE_PATH


# args validation
if GOOGLE_API_KEY == "":
    raise Exception("Google API key cannot be empty")
util.pathExist(PLACE_ID_FILE_PATH)
util.pathWritable(DISTANCE_DATA_FILE_PATH)


def main():
    with open(PLACE_ID_FILE_PATH) as f:
        placeIdList = f.read().splitlines()
        placeIdList = util.removeEmptyElem(placeIdList)
    print("Loaded {} places from the given file".format(len(placeIdList)))
    diagonalPlaceIdCombinations = [(placeIdList[i], placeIdList[j])
                                   for i in range(len(placeIdList))
                                   for j in range(len(placeIdList))[i+1:]]
    urls = []
    for combo in diagonalPlaceIdCombinations:
        urls += formRequestUrls(combo[0], combo[1])
    results = fetchData.requestDataFromUrls(urls)
    util.writeToPath(json.dumps(results), DISTANCE_DATA_FILE_PATH)
    print("Saved {} results to {}".format(len(results),
                                          DISTANCE_DATA_FILE_PATH))


# Returns a list of request URLs to fetch data from Google place
def formRequestUrls(placeId1, placeId2):
    return list(map(lambda travelMode: "https://maps.googleapis.com/maps/api/directions/json?origin=place_id:{}&destination=place_id:{}&mode={}&key={}".format(
        placeId1, placeId2, travelMode, GOOGLE_API_KEY
    ), ["driving", "walking", "bicycling", "transit"]))


main()
