import os
import sys


if sys.version_info[0] < 3:
    raise Exception("Must be using Python 3")


def loadEnv(var):
    return os.environ[var] if var in os.environ else ""


# loading environment variables
GOOGLE_API_KEY = loadEnv("GOOGLE_API_KEY")
LATITUDE = loadEnv("LATITUDE")
LONGITUDE = loadEnv("LONGITUDE")
PLACE_ID_FILE_PATH = loadEnv("PLACE_ID_FILE_PATH")
DISTANCE_DATA_FILE_PATH = loadEnv("DISTANCE_DATA_FILE_PATH")
CSV_DATA_FILE_PATH = loadEnv("CSV_DATA_FILE_PATH")
BUDGET = loadEnv("BUDGET")
CONCURRENCY = loadEnv("CONCURRENCY")


# Helpers for lists

def removeEmptyElem(elemList):
    return [elem for elem in elemList if elem != ""]


# split a list into a given number of chunks
def splitListIntoChunks(l, chunkNum):
    return list(chunks(l, chunkNum))


def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]


# Helpers for file system

def pathExist(path):
    if not os.path.exists(path):
        raise Exception("The given path %s does not exist" % path)


def pathWritable(path):
    try:
        f = open(path, "w+")
        f.close()
    except IOError:
        raise Exception("Cannot write to the given path: %s" % path)


def writeToPath(result, path):
    if isinstance(result, str):
        outputFile = open(path, "w+")
        outputFile.write(result)
        outputFile.close()
    else:
        raise Exception("Cannot write non-string to file")
