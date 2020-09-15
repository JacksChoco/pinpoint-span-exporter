import sys
import time
import json
import requests
import datetime
import math
import os
from prometheus_client import start_http_server, Gauge, Info, Histogram

## getScatterData -> transcationId
PINPOINT_URL = "http://125.209.240.10:10123"
def extract_cost(json):
    try: 
        # Also convert to int since update_time will be string.  When comparing
        # strings, "10" is smaller than "2".
        return json['totCost']
    except KeyError:
        print(json)
        return 0

def info_service(info):
    res = requests.get("{}/applications.pinpoint".format(PINPOINT_URL))
    service_list = []
    for service in res.json():
        info.labels(service["applicationName"], service["serviceType"]).set(1)
        service_list.append(service["applicationName"])
    return service_list

def get_transactionId(application):
    ts = int(datetime.datetime.now().timestamp()) * 1000
    print(ts)
    url = "{}/getScatterData.pinpoint?application={}&from={}&to={}&xGroupUnit=23478&yGroupUnit=43&limit=5000&backwardDirection=true&filter=".format(PINPOINT_URL,application,ts-600000,ts)
    print(url)
    res = requests.get(url)
    metadata = res.json()["scatter"]["metadata"]
    dotList = res.json()["scatter"]["dotList"]
    transactionList = []
    
    for dot in dotList:
        transactionId = "{}^{}^{}".format(metadata[str(dot[2])][1],metadata[str(dot[2])][2],dot[3])
        transactionList.append({
            "transactionId": transactionId,
            "success": dot[4],
            "duration": dot[0],
        })
    return transactionList
    
def gauge_span(transactionList,duration):  
    for transaction in transactionList:
        print(transaction["transactionId"])
        url = "{}/transactionInfo.pinpoint?traceId={}".format(PINPOINT_URL,transaction["transactionId"])
        res = requests.get(url)
        callStack = res.json()['callStack']
        duration.labels("aa","bb").observe(int(callStack[0][14]))
        for call in callStack:
            if call[8]:
                gapTime = call[13]
                execTime = call[14]
                selfTime = call[16]
                className = call[17]
                apiName = call[19]
                #print("gap: {},exec: {}ms,self: {}ms,class: {},api: {}".format(gapTime,execTime,selfTime,className,apiName))
            
    return

if __name__ == '__main__':
    # start the server
    start_http_server(8005)
    print("run server")
    info = Gauge('pinpoint_service_info', 'aws price detail',('service','type'))
    duration = Histogram('pinpoint_service_api_duration', 'aws price detail',('service','type')) 
    try:
        while True:
            service_list = info_service(info)
            for service in service_list:
                gauge_span(get_transactionId(service),duration)
            time.sleep(3600)
            
    except KeyboardInterrupt:
        print('\nYou killed Kenny, you bastard!\n')
        sys.exit()