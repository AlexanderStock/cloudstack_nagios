import json

def inventory_cloudstack_hvstatus(info):
    data=json.loads(info)
    for line in data:
        yield line['name']

def check_cloudstack_hvstatus(item, params, info):
    data = json.loads(info)
    thresholds={}
    for hv in data:
        if hv['name'] == item:
            if hv['name'] in params:
                thresholds = params[hv['name']]
            return check_hvstatus(resource=[hv],thresholds=thresholds)


check_info["check_cloudstack_hvstatus"] = {
    'check_function':            check_cloudstack_hvstatus,
    'inventory_function':        inventory_cloudstack_hvstatus,
    'service_description':       'HV Status',
    'has_perfdata':              True,
    'group':                     'check_cloudstack_hvstatus',
    'includes':                  ['cschecks.include'],
}