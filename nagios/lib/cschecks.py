#!/usr/bin/python
# by Alexander Stock
#
import copy

############################
#### Check definitions #####
############################

def check_capacity(resource=None,thresholds={}):
    types = {
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
    message="See long output: \n<pre>\n"
    exitcode=0
    performancedata=[]
    name=types[resource['type']]
    warn = 0
    critical = 0
    if 'warn' in thresholds and 'critical' in thresholds:
        warn=thresholds['warn']
        critical=thresholds['critical']
        if resource['percentused'] > warn and resource['percentused'] < critical:
            message=message + "WARN:     {:40} has reached warning value. Threshold:{}% Value:{}%\n".format(name,warn,resource['percentused'])
            if exitcode < 1:
                exitcode=1
        elif resource['percentused'] > critical:
            message=message + "Critical: {:40} has reached warning value. Threshold:{}% Value:{}%\n".format(name,critical,resource['percentused'])
            if exitcode < 2:
                exitcode=2
        else:
            message = message + "OK:       {:40} is in status ok. Value:{}% \n".format(name,resource['percentused'])
    else:
        message = message + "OK:       {:40} No Thresholds given. Value:{}%\n".format(name,resource['percentused'])

        # Add Performance data
        performancedata.append((name, resource['percentused'] + "%", warn, critical, ''))

    message += "</pre>\n"
    return exitcode,message,performancedata

def check_virtualrouter(resource=None,thresholds={}):

    message="See long output: \n<pre>Name       Status   Running    Upgrade\n"
    vpcmessage="Status of redundant VPC Routers\nName    Status        Status\n"
    exitcode=0
    performancedata=[]
    vpcdict = {}
    shutdownrouters=0
    updaterouters=0

    for router in resource:
        name=router['name']
        status="OK"
        running="yes"
        upgrade="no"
        if router['state'] != 'Running':
            running="no"
            status = "Critical"
            shutdownrouters+=1
            if exitcode < 2:
                exitcode = 2

        if router['requiresupgrade'] is not False:
            upgrade="yes"
            updaterouters+=1
            status = "Critical"
            if exitcode < 2:
                exitcode = 2

        if router['isredundantrouter']:
            vpc=router['vpcname']
            if router['vpcname'] not in vpcdict:
                vpcdict[router['vpcname']]={}
            vpcdict[vpc][name] = router['redundantstate']

        message="{:10}{:10}{:10}{:10}{:10}\n".format(message,name,status,running,upgrade)

    for vpc in vpcdict.keys():
        mastercount=0
        routercount=0
        for router in vpcdict[vpc].keys():
            routercount+=1
            if vpcdict[vpc][router] == "MASTER":
                mastercount+=1
        if mastercount == 1:
            vpcmessage=vpcmessage + vpc + "    OK            Two Routers found with one as master\n"
        if mastercount < 1:
            vpcmessage = vpcmessage + vpc + "    Crit            No MASTER found\n"
        if mastercount > 2:
            vpcmessage = vpcmessage + vpc + "    Crit           No MASTER found\n"

    message=message+"\n"+vpcmessage

    #Add Performance data
    performancedata.append(("Needs_Update", updaterouters,'','','' ))
    performancedata.append(("Not_running", shutdownrouters, '', '', ''))

    message += "</pre>\n"
    return exitcode,message,performancedata

def check_systemvm(resource=None,thresholds={}):

    message="See long output: \n<pre>"
    exitcode=0
    shutdownvms=0
    performancedata=[]

    for vm in resource:
        if vm['state'] != "Running":
            message=message+"Critical: " + vm['name'] + " is not running. \n"
            shutdownvms+=1
            if exitcode < 2:
                exitcode = 2
        else:
            message = message + "OK: " + vm['name'] + " is running. \n"

    #Add Performance data
    performancedata.append(("Not_running", shutdownvms, '', '', ''))

    message += "</pre>\n"
    return exitcode,message,performancedata

def check_projects(resource=None,thresholds={}):

    message="See long output: \n<pre>"
    exitcode=0
    performancedata=[]
    values=[
        "cpu",
        "ip",
        "memory",
        "network",
        "primarystorage",
        "secondarystorage",
        "snapshot",
        "template",
        "vm",
        "volume",
        "vpc"]

    for project in resource:
        message+="\nResults for Project "+ project['name'] +":"
        for value in  values:
            warn = None
            crit = None
            if project[value+'limit'] != "Unlimited" \
            and project[value+'limit'] != "0" \
            and project[value+'total'] != "Unlimited":
                percentvalue = (int(project[value+'total'])/int(project[value+'limit']))*100
                identifier=project['domain']+"-"+project['name']
                if identifier in thresholds:
                    if value in thresholds[project['name']]:
                        warn = thresholds[project['name']][value]['warn']
                        crit = thresholds[project['name']][value]['critical']
                    else:
                        if "global" in thresholds:
                            if value in thresholds['global']:
                                warn = thresholds['global'][value]['warn']
                                crit = thresholds['global'][value]['critical']

                if warn != None and crit != None:
                    if int(warn) < percentvalue and int(crit) > percentvalue:
                        message += "\n--> Warning: Project " + str(project['name']) + " has reached threshold for " + value + ": " + str(percentvalue)
                        exitcode = 1
                    elif int(crit) < percentvalue:
                        message += "\n--> Critical: Project " + str(project['name']) + " has reached threshold for " + value + ": " + str(percentvalue)
                        exitcode = 2

                performancedata.append((project['domain']+"+"+project['name']+"+usage" + "!" + value, percentvalue, '', '', ''))
                performancedata.append((project['domain'] + "+" + project['name'] + "+total" + "!" + value,project[value+'total'], '', '', ''))
            else:
                if project[value+'total'] != "Unlimited":
                    performancedata.append((project['domain'] + "+" + project['name'] + "+total" + "!" + value,project[value + 'total'], '', '', ''))
                else:
                    performancedata.append((project['domain'] + "+" + project['name'] + "+total" + "!" + value,-1, '', '', ''))

                performancedata.append((project['domain'] +"+" + project['name'] + "+usage" + "!" + value, -1, '', '', ''))

    message += "</pre>\n"
    return exitcode,message,performancedata

def check_domains(resource=None,thresholds={}):

    message="See long output: \n<pre>"
    exitcode=0
    performancedata=[]
    values=[
        "cpu",
        "ip",
        "memory",
        "network",
        "primarystorage",
        "secondarystorage",
        "snapshot",
        "template",
        "vm",
        "volume",
        "vpc"]

    for domain in resource:
        message+="\nResults for Domain "+ domain['name'] +":"
        for value in  values:
            warn=None
            crit=None
            if domain[value+'limit'] != "Unlimited" \
            and domain[value+'limit'] != "0" \
            and domain[value+'total'] != "Unlimited":
                percentvalue = (int(domain[value+'total'])/int(domain[value+'limit']))*100
                if domain['name'] in thresholds['domains']:
                    if value in thresholds['domains'][domain['name']]:
                        warn=thresholds['domains'][domain['name']][value]['warn']
                        crit=thresholds['domains'][domain['name']][value]['critical']
                    else:
                        if "global" in thresholds:
                            if value in thresholds['global'] and domain[value] != "Unlimited":
                                warn=thresholds['global'][value]['warn']
                                crit=thresholds['global'][value]['critical']

                if warn != None and crit != None:
                    if int(warn) > percentvalue and int(crit) < percentvalue:
                        message +="\n--> Warning: Domain " + str(domain['name']) + " has reached threshold for " + value + ": " + str(percentvalue)
                        exitcode = 1
                    elif int(crit) > percentvalue:
                        message+="\n--> Critical: Domain " + str(domain['name']) +" has reached threshold for " + value + ": " + str(percentvalue)
                        exitcode = 2
                performancedata.append((domain['name'] + "+usage" + "!" + value, percentvalue, '', '', ''))
                performancedata.append((domain['name'] + "+total" + "!" + value, domain[value + 'total'], '', '', ''))
            else:
                if domain[value + 'total'] != "Unlimited":
                    performancedata.append((domain['name'] + "+total" + "!" + value,domain[value + 'total'], '', '', ''))
                else:
                    performancedata.append((domain['name'] + "+total" + "!" + value, -1, '', '', ''))
                performancedata.append((domain['name'] + "+usage" + "!" + value, -1, '', '', ''))

    message += "</pre>\n"
    return exitcode,message,performancedata

def check_hvstatus(resource=None,thresholds={}):

    message="See long output: \n<pre>\n"
    exitcode=0
    shutdownhosts={}
    disabledhosts={}
    performancedata=[]
    lastcluster=""

    for host in sorted(resource,key=lambda x: x['clustername']):
        result = "OK"
        status = "running"
        enabled = "yes"
        if host['clustername'] not in shutdownhosts:
            shutdownhosts[host['clustername']] = 0
        if host['clustername'] not in disabledhosts:
            disabledhosts[host['clustername']] = 0
        if host['state'] != "Up":
            result="Critical"
            status = "not running"
            shutdownhosts[host['clustername']]+=1
            if exitcode < 2:
                exitcode = 2
        if host['resourcestate'] != "Enabled":
            result="Critical"
            enabled="no"
            disabledhosts[host['clustername']]+=1
            if exitcode < 2:
                exitcode = 2
        if lastcluster != host['clustername']:
            message+="Status for Cluster: " + host['clustername'] + "\n"
            message+="Host       Result      Status  Enabled\n".format(result,host['name'],status,enabled)
        lastcluster=host['clustername']
        message = message + "{:10} {:10}  {} {:10}\n".format(host['name'],result,status,enabled)

    #Add Performance data
    for entry in shutdownhosts.keys():
        performancedata.append((entry+"!Not_running", shutdownhosts[entry], '', '', ''))
    for entry in disabledhosts.keys():
        performancedata.append((entry+"!Not_enabled", disabledhosts[entry], '', '', ''))

    message += "</pre>\n"
    return exitcode,message,performancedata

def check_offerings(resource=None,thresholds={}):

    offerings = resource['offerings']
    clusters = resource['cluster']
    offeringdict={}
    errors=""
    performancedata=[]
    message="See long output: \n<pre>"

    for cluster in clusters:
        clustername = cluster[0]
        hvstatus=cluster[1]
        for offering in sort_objects(offerings['serviceoffering'], "cpunumber", "memory"):
            if offering['iscustomized'] is False:
                #Simulate offering deployment
                (temphvstatus, tempdistribution, tempmem, tempcpu)=deploy_offerings(offering, hvstatus)
                if offering['name'] not in offeringdict:
                    offeringdict[offering['name']]=0
                offeringdict[offering['name']]+=tempdistribution[offering['name']]

        header = "\n!  Offering! Count!\n"
        for offering in sorted(offeringdict.keys()):
            if offering in thresholds:
                warn = thresholds[offering]['warn']
                critical = thresholds[offering]['critical']
                if offeringdict[offering] >= warn and offeringdict[offering] <= critical:
                    errors+="--> Warn: Offering: " + offering + " has broke threshold:" + warn + " with "+ str(offeringdict[offering]) + "\n"
                    if exitcode < 2:
                        exitcode = 1
                elif offeringdict[offering] <= critical:
                    errors += "--> Critical: Offering: " + offering + " has broke threshold:" + critical + " with " + str(offeringdict[offering]) + "\n"
                    exitcode = 2
            if offeringdict[offering] == 0:
                errors += "--> Critical: Offering: " + offering + " can not be deployed anymore\n"
                exitcode=1
            header+="!{:10}!{:6}!\n".format(offering,offeringdict[offering])
            performancedata.append((clustername+"!"+offering +"-count",offeringdict[offering], '', '', ''))

        message+="\nStatistics for Cluster: " + clustername + "\n"
        message+=header
        message+="\n"+errors

    message+="</pre>\n"
    return exitcode,message,performancedata



########################################################################################################
##############                          Helper Functions                                  ##############
########################################################################################################

def sort_objects(array,cpuvalue,memvalue):

    resultarray = []
    for i in range(0,len(array)):
        offer = array[i]
        if memvalue in offer and cpuvalue in offer:
            ratio=offer[memvalue]*offer[cpuvalue]
            if i == 0:
                resultarray.insert(0,offer)
            else:
                rankingposition = len(resultarray)
                for result in reversed(resultarray):
                    resultratio = result[memvalue]*result[cpuvalue]

                    if offer[cpuvalue] >= result[cpuvalue] and offer[memvalue] >= result[memvalue]:
                        rankingposition -= 1
                    elif offer[cpuvalue] >= result[cpuvalue] and offer[memvalue] <= result[memvalue] and ratio >= resultratio:
                        rankingposition -= 1
                    elif offer[cpuvalue] <= result[cpuvalue] and offer[memvalue] >= result[memvalue] and ratio >= resultratio:
                        rankingposition -= 1

                resultarray.insert(rankingposition, offer)
    return(resultarray)

def deploy_offerings(offering,hvorig):

    newcpu = 0
    newmem = 0
    distribution={}
    distribution[offering['name']] = 0
    cpu = (offering['cpuspeed'] * offering['cpunumber'])
    mem = offering['memory'] * 1024
    hvlist=copy.deepcopy(hvorig)

    # Deploy on original HVs
    for hv in hvlist:
        memfactor = int(hv['memfree'] / mem)
        cpufactor = int(hv['cpufree'] / cpu)
        if memfactor > 1 and cpufactor > 1:
            if memfactor > cpufactor:
                distribution[offering['name']] += cpufactor
                newcpu += cpufactor * cpu
                newmem += cpufactor * mem
                hv['cpufree'] -= cpu * cpufactor
                hv['memfree'] -= mem * cpufactor
            if memfactor < cpufactor:
                distribution[offering['name']] += memfactor
                newcpu+= memfactor * cpu
                newmem += memfactor * mem
                hv['cpufree'] -= cpu * memfactor
                hv['memfree'] -= mem * memfactor

    return hvlist,distribution,newmem,newcpu