#!/bin/bash
set -ex

# This script will configure the environment then run
# fetchPlaceIdData.py, fetchDistanceData.py, and dataCleaning.py
# scripts in order to fetch and generate training data.

# Environment Variable Configuration
export GOOGLE_API_KEY=""            # Google Place API Key
export LATITUDE=""                  # Latitude of the starting point
export LONGITUDE=""                 # Longitude of the starting point
export PLACE_ID_FILE_PATH=""        # Place ID list file
export DISTANCE_DATA_FILE_PATH=""   # Travel info file returned from Google
export CSV_DATA_FILE_PATH=""        # Features extracted from Google travel info
export BUDGET=1000                  # Max number of Google API calls allowed to send for each script
export CONCURRENCY=16               # The number of threads used to fetch data

# Every script has customized arg validations, and they are independent of each other.
# So, you can execute them seprately by commenting out the privious commands.
python3 fetchPlaceIdData.py
python3 fetchDistanceData.py
python3 dataCleaning.py
