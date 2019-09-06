#!/usr/bin/python
# by Alexander Stock
from check_mk.checks.check_cloudstack_domains import inventory_cloudstack_domains,check_cloudstack_domains
from nagios.lib import csresources
import json

csr = csresources()
print inventory_cloudstack_domains(json.dumps(csr.list_domains()))
print check_cloudstack_domains("test1",{},json.dumps(csr.list_domains()))