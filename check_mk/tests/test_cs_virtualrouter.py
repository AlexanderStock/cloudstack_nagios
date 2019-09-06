#!/usr/bin/python
# by Alexander Stock
from check_mk.checks.check_cloudstack_projects import inventory_cloudstack_projects,check_cloudstack_projects
from nagios.lib import csresources
import json

csr = csresources()
print inventory_cloudstack_projects(json.dumps(csr.list_projects()))
print check_cloudstack_projects("Quadrio/quadrio",{},json.dumps(csr.list_projects()))