import json

def inventory_cloudstack_systemvm(info):
    yield "", None

def check_cloudstack_systemvm(item, params, info):
    data = json.loads(str(info[0][0]))
    thresholds={}
    return check_systemvm(resource=data,thresholds=thresholds)


check_info["check_cloudstack_systemvm"] = {
    'check_function':            check_cloudstack_systemvm,
    'inventory_function':        inventory_cloudstack_systemvm,
    'service_description':       'CloudStack SystemVM',
    'has_perfdata':              True,
    'group':                     'check_cloudstack_systemvm',
    'includes':                  ['cschecks.include'],
}