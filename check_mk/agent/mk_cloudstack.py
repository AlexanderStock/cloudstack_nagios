#!/usr/bin/python
# by Alexander Stock
from . import csresources
import json

myResult = ""
csr = csresources()

#Get Capacity
myResult += "<<<cloudstack_capacity>>>\n"
myResult += json.dumps(csr.list_capacity())+"\n"

#Get virtual routers
myResult += "<<<cloudstack_virtualrouter>>>\n"
myResult += json.dumps(csr.list_virtual_routers())+"\n"

#Get hypervisors
myResult += "<<<cloudstack_hypervisors>>>\n"
myResult += json.dumps(csr.list_hvs())+"\n"

#Get system VMs
myResult += "<<<cloudstack_systemvm>>>\n"
myResult += json.dumps(csr.list_system_vms())+"\n"

#Get projects
myResult += "<<<cloudstack_projects>>>\n"
myResult += json.dumps(csr.list_projects())+"\n"

#Get domains
myResult += "<<<cloudstack_domains>>>\n"
myResult += json.dumps(csr.list_domains())+"\n"

#Get offerings
first=1
myResult += "<<<cloudstack_offerings>>>\n"
myResult += "<cluster>\n"
myTmpOutput = []
for cluster in csr.list_clusters():
    myTmpOutput.append([cluster['name'],csr.get_hvstructure(cluster,withvm=1)])
    first = 1
myResult += json.dumps(myTmpOutput)
myResult += "\n"
myResult += "<offerings>\n"
myResult += json.dumps(csr.list_offerings())

#Remove all whitespace
myResult.replace(" ", "")
#Return string
print myResult