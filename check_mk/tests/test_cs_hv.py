#!/usr/bin/python
# by Alexander Stock
from check_mk.checks.mk_cs_hvstatus import inventory_cloudstack_hvstatus,check_cloudstack_hvstatus
from nagios.lib import csresources
import json

csr = csresources()
print inventory_cloudstack_hvstatus(json.dumps(csr.list_hvs()))
print check_cloudstack_hvstatus("SimulatedAgent.403f257b-57b9-4d27-baf8-26dac9dac22a",{},json.dumps(csr.list_hvs()))

