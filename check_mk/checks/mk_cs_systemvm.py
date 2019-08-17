def inventory_cloudstack_systemvm(info):
    yield ""

def check_cloudstack_systemvm(item, params, info):
    thresholds={}
    return check_systemvm(resource=info,thresholds=thresholds)


check_info["check_cloudstack_systemvm"] = {
    'check_function':            check_cloudstack_systemvm,
    'inventory_function':        inventory_cloudstack_systemvm,
    'service_description':       'SystemVMs',
    'has_perfdata':              True,
    'group':                     'check_cloudstack_systemvm',
    'includes':                  ['cschecks.include'],
}