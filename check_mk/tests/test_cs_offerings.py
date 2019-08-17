#!/usr/bin/python
# by Alexander Stock
from check_mk.checks.mk_cs_offering import inventory_cloudstack_offerings,check_cloudstack_offerings
from nagios.lib import csresources
import json

first = 1
csr = csresources()
myResult=""
myResult += "<cluster>\n["
for cluster in csr.list_clusters():
    if first == 1:
        delimiter=""
    else:
        delimiter = ","
    myResult += delimiter + json.dumps([cluster['name'],csr.get_hvstructure(cluster,withvm=1)])
    first = 0
myResult += "]\n"
myResult += "<offerings>\n"
myResult += json.dumps(csr.list_offerings())

print inventory_cloudstack_offerings(myResult)
print check_cloudstack_offerings("XXXL",{},myResult)