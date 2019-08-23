# Commute Time Estimation

Fetching data from Google for analyzing commute pattern in a city. This contains three main models: `fetchPlaceIdData`, `fetchDistanceData`, and `dataCleaning`. You should setup required environment variables by modifying `start.sh`, then you can start the process by running `./start.sh`. After the process is done, three files will be generated, one for storing place id, one for returned commute information, and one for processed csv data.

By specifying a starting geopoint in a city, the `fetchPlaceIdData.py` script will fetch its nearby places from Google, then request from Google what is the commute time required between every two places. The commute type includes "driving", "walking", "bicycling", "transit". Finally, it generates a csv file in this format `distance,lat1,lng1,lat2,lng2,steps,mode,requestTime,duration` for further data analysis.

The scripts require `python 3`.

Please refer to each file for detailed explainations.

![Powered by Google](res/powered_by_google_on_white_hdpi.png)