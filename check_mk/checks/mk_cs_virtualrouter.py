def inventory_cloudstack_virtualrouter(info):
    yield ""

def check_cloudstack_virtualrouter(item, params, info):
    thresholds={}
    return check_virtualrouter(resource=info,thresholds=thresholds)


check_info["check_cloudstack_virtualrouters"] = {
    'check_function':            check_cloudstack_virtualrouter,
    'inventory_function':        inventory_cloudstack_virtualrouter,
    'service_description':       'Virtual Routers',
    'has_perfdata':              True,
    'group':                     'check_cloudstack_virtualrouters',
    'includes':                  [ 'cschecks.include' ],
}