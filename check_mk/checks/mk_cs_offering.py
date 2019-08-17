import re
import json

def inventory_cloudstack_offerings(info):
    foundOffering = False
    for line in info:
        if re.search("^<offerings>", line) is not None:
            foundOffering = True
        if foundOffering == True:
            data = json.loads(line)
            for offering in data:
                yield offering["name"]

def check_cloudstack_offerings(item, params, info):
    thresholds = {}
    myOffering = []
    myCluster = []
    foundOffering = False
    foundCluster = False
    for line in info.split("\n"):
        #Search for offering tag
        if re.search("^<offerings>*",line) is not None:
            foundOffering = True
            foundCluster = False
            continue
        #Search for cluster tag
        if re.search("^<cluster>*", line) is not None:
            foundCluster = True
            foundOffering = False
            continue
        #Find offering in Data
        if foundOffering == True:
            for offering in json.loads(line):
                if item == offering["name"]:
                    if offering["name"] in params:
                        thresholds = params[offering["name"]]
                    myOffering=offering
        if foundCluster == True:
            myCluster=json.loads(line)

    metric=[[myOffering],myCluster]
    return check_offerings(resource=metric,thresholds=thresholds)


check_info["check_cloudstack_offerings"] = {
    'check_function':            check_cloudstack_offerings,
    'inventory_function':        inventory_cloudstack_offerings,
    'service_description':       'Count for offering %s',
    'has_perfdata':              True,
    'group':                    'check_cloudstack_offerings',
    'includes':                 ['cschecks.include'],
}