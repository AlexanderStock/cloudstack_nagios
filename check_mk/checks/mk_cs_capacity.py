import json

cs_types = {
    0: 'CAPACITY_TYPE_MEMORY',
    1: 'CAPACITY_TYPE_CPU',
    2: 'CAPACITY_TYPE_STORAGE',
    3: 'CAPACITY_TYPE_STORAGE_ALLOCATED',
    4: 'CAPACITY_TYPE_VIRTUAL_NETWORK_PUBLIC_IP',
    5: 'CAPACITY_TYPE_PRIVATE_IP',
    6: 'CAPACITY_TYPE_SECONDARY_STORAGE',
    7: 'CAPACITY_TYPE_VLAN',
    8: 'CAPACITY_TYPE_DIRECT_ATTACHED_PUBLIC_IP',
    19: 'CAPACITY_TYPE_LOCAL_STORAGE',
}

def inventory_cloudstack_capacity(info):
    data=json.loads(info)
    for line in data:
        if line['type'] in cs_types:
            yield cs_types[line['type']]


def check_cloudstack_capacity(item, params, info):
    thresholds={}
    data = json.loads(info)
    for metric in data:
        if cs_types[metric['type']] == item:
            if cs_types[metric['type']] in params:
                thresholds = params[cs_types[metric['type']]]
            return check_capacity(resource=metric,thresholds=thresholds)


check_info["check_cloudstack_capacity"] = {
    'check_function':            check_cloudstack_capacity,
    'inventory_function':        inventory_cloudstack_capacity,
    'service_description':       'Capacity for %s',
    'has_perfdata':              True,
    'group':                     'check_cloudstack_capacity',
    'includes':                  ['cschecks.include'],
}