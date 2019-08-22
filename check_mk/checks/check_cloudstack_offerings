import re
import json

def inventory_cloudstack_offerings(info):
    foundOffering = False
    for line in info:
        if foundOffering == True:
            data = json.loads(line[0])
            for offering in data:
                yield offering["name"], None
        foundOffering = False
        if re.search("<offerings>",line[0]) is not None:
            foundOffering = True


def check_cloudstack_offerings(item, params, info):
    thresholds = {}
    myOffering = []
    myCluster = []
    foundOffering = False
    foundCluster = False
    for line in info:
        #Search for offering tag
        if re.search("<offerings>",line[0]) is not None:
            foundOffering = True
            foundCluster = False
            continue
        #Search for cluster tag
        if re.search("<cluster>", line[0]) is not None:
            foundCluster = True
            foundOffering = False
            continue
        #Find offering in Data
        if foundOffering == True:
            for offering in json.loads(line[0]):
                if item == offering["name"]:
                    if params is not None:
                        if offering["name"] in params:
                            thresholds = params[offering["name"]]
                    myOffering = offering
        if foundCluster == True:
            #for cluster in line[0]:
            #    print cluster[0]
                #cluster[0] = cluster[0].encode("utf-8")
            del line[0][2]
            myCluster = json.loads(line[0])

    metric=[[myOffering],myCluster]
    return check_offerings(resource=metric,thresholds=thresholds)

def unicode_to_string(info):
   for line in info:
       line[0] = line[0].encode("utf-8")
   return info

check_info["check_cloudstack_offerings"] = {
    'check_function':            check_cloudstack_offerings,
    'inventory_function':        inventory_cloudstack_offerings,
    'parse_function':            unicode_to_string,
    'service_description':       'CloudStack Count for offering %s',
    'has_perfdata':              True,
    'group':                    'check_cloudstack_offerings',
    'includes':                 ['cschecks.include'],
}