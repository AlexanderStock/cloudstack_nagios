#!/usr/bin/python
# by Alexander Stock
from check_mk.checks.check_cloudstack_capacity import inventory_cloudstack_capacity,check_cloudstack_capacity
from nagios.lib import csresources
import json

csr = csresources()
print inventory_cloudstack_capacity(json.dumps(csr.list_capacity()))
print check_cloudstack_capacity("CAPACITY_TYPE_VLAN",{},json.dumps(csr.list_capacity()))