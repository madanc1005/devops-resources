import requests
import time
import os
import csv
from datetime import datetime

            
def checkUrl(urls):
    outPut = [
        ["Timestamp", "URL", "Status", "Status Code",
         "Response Time (s)", "Error"]
    ]
    for url in urls:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        startTime = time.time()
        try:
            response = requests.get(url, timeout=10)
            responseTime = time.time() - startTime
            statusCode = response.status_code
            if statusCode == 200:
                status = "UP"
            else:
                status = "DOWN"
            error = "N/A"
        except requests.exceptions.RequestException as e:
            responseTime = time.time() - startTime
            status = "ERROR"
            statusCode = "N/A"
            error = str(e)
        outPut.append([
            timestamp, url, status, statusCode,
            round(responseTime, 2), error
        ])
        print(url, status, statusCode, error)
    return outPut

def listTheData(inputdata):
    urls =[]
    try:
        if  os.path.exists(inputdata):
            with open(inputdata, "r", newline="") as csvfile:
                csvData = csv.reader(csvfile)
                next(csvData,None)
                for row in csvData:
                    if row and row[0].strip():
                        urls.append(row[0].strip())
                return urls
    except Exception as e:
        print("the file is not exist")

def writeData(results,outputData):
    try:
        with open(outputData,"w") as csvfile:
            write = csv.writer(csvfile)
            write.writerows(results)
        print("data is written into the csv file")
    except Exception as e :
        print("error while wrting csv file : "+str(e))
    

def main():
    inputData = "web_services.csv"
    outputData = "h_c_r.csv"
    urls = listTheData(inputData)
    results = checkUrl(urls)
    writeData(results,outputData)

if __name__ == "__main__":
    main()
