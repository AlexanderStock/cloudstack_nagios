import json

def inventory_cloudstack_domains(info):
    data = json.loads(info)
    for line in data:
       yield line['type']

def check_cloudstack_domains(item, params, info):
    data = json.loads(info)
    thresholds={}
    for metric in data:
        if metric['name'] == item:
            if metric['name'] in params:
                thresholds = params[metric['name']]
                if thresholds == {}:
                    thresholds = {'domains':{}}
            return check_domains(resource=[metric],thresholds=thresholds)


check_info["check_cloudstack_domains"] = {
    'check_function':            check_cloudstack_domains,
    'inventory_function':        inventory_cloudstack_domains,
    'service_description':       'Capacity for domain %s',
    'has_perfdata':              True,
    'group':                     'check_cloudstack_domains',
    'includes':                  ['cschecks.include'],
}