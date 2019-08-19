#!/usr/bin/python
# by Alexander Stock
from check_mk.checks.check_cloudstack_systemvm import inventory_cloudstack_systemvm,check_cloudstack_systemvm
from nagios.lib import csresources
import json

csr = csresources()
print inventory_cloudstack_systemvm(json.dumps(csr.list_projects()))
print check_cloudstack_systemvm("Quadrio/quadrio",{},json.dumps(csr.list_projects()))