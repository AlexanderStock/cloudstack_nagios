import json

def inventory_cloudstack_projects(info):
    for line in info:
       yield line['domain']+"/"+line['name']

def check_cloudstack_projects(item, params, info):
    data = json.loads(info)
    thresholds={}
    for metric in data:
        domainpath=metric['domain']+"/"+metric['name']
        if domainpath == item:
            if domainpath in params:
                thresholds = params[domainpath]
            return check_projects(resource=[metric],thresholds=thresholds)


check_info["check_cloudstack_projects"] = {
    'check_function':            check_cloudstack_projects,
    'inventory_function':        inventory_cloudstack_projects,
    'service_description':       'Capacity for project %s',
    'has_perfdata':              True,
    'group':                     'check_cloudstack_projects',
    'includes':                  ['cschecks.include'],
}