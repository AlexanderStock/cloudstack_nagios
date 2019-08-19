import json

def inventory_cloudstack_virtualrouter(info):
    yield "", None

def check_cloudstack_virtualrouter(item, params, info):
    thresholds={}
    data = json.loads(str(info[0][0]))
    return check_virtualrouter(resource=data,thresholds=thresholds)


check_info["check_cloudstack_virtualrouter"] = {
    'check_function':            check_cloudstack_virtualrouter,
    'inventory_function':        inventory_cloudstack_virtualrouter,
    'service_description':       'CloudStack Virtual Routers',
    'has_perfdata':              True,
    'group':                     'check_cloudstack_virtualrouters',
    'includes':                  [ 'cschecks.include' ],
}