import json
import multiprocessing
import requests
import time
import util

""" Multi-processing data fetching model

Fetch data as per concurrency and budget settings.
Use multiprocessing model as the task is CPU intensive.
"""


# loading environment variables
BUDGET = util.BUDGET
CONCURRENCY = util.CONCURRENCY


# args validation
try:
    BUDGET = int(BUDGET)
    CONCURRENCY = int(CONCURRENCY)
    print("The script executes with %d threads and %d is the maximum budget allowed." % (
        CONCURRENCY, BUDGET))
except:
    raise Exception("Both budget and concurrency must be integer")


# Multiprocessing setup
mutex = multiprocessing.Lock()


# Requesting data
def requestDataFromUrls(urls):
    total = len(urls) if len(urls) < BUDGET else BUDGET
    print("There will be {} requests to send".format(total))
    return requestDataFromUrlsMultiprocess(urls[:total])


# Assume: the parameter should have considered budget effects.
def requestDataFromUrlsMultiprocess(urls):
    if len(urls) > CONCURRENCY:
        # (len(urls) / CONCURRENCY) + 1 makes sure every url will get a spot
        urlSubsets = util.splitListIntoChunks(
            urls, int(len(urls) / CONCURRENCY) + 1)
    else:
        urlSubsets = [[i] for i in urls]
    jobs = []
    counter = multiprocessing.Value("i", 0)
    success = multiprocessing.Value("i", 0)
    manager = multiprocessing.Manager()
    results = manager.list()
    for i in range(len(urlSubsets)):
        urlSubset = urlSubsets[i]
        p = multiprocessing.Process(
            target=requestDataFromUrlsSingleProcess,
            args=(urlSubset, counter, success, len(urls), i, results))
        jobs.append(p)
        p.start()
    [job.join() for job in jobs]
    print("Process finished. {} out of {} requests were successed".format(
        success.value, len(urls)))
    return list(results)


def requestDataFromUrlsSingleProcess(urls, counter, success, total, index, results):
    result = []
    for url in urls:
        with mutex:
            counter.value += 1
            print("Processing {} out of {} urls. {}% done.".format(
                counter.value, total, int(counter.value * 100 / total)))
        result = fetchDataFromGoogleAPI(url)
        if result != "":
            success.value += 1
            results.append(result)
    return


def fetchDataFromGoogleAPI(url):
    res = requests.get(url)
    if res.status_code != 200:
        print("Failed fetching data with status {}\nMessage: {}".format(
            res.status_code, res.text))
        return ""
    result = res.json()
    if result["status"] != "OK":
        print("Google returned a non-success response:\n{}".format(str(result)))
        return ""
    result["requestTimestamp"] = time.time()
    return json.dumps(result)
