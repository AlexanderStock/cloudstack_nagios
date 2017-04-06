#!/usr/bin/python
# by Alexander Stock
#
import getopt
import sys
import copy
import os
import json
from cs import CloudStack

class check_cs:

    def __init__(self):
        try:
            self.myopts, self.args = getopt.getopt(sys.argv[1:], "f:m:d:p:c")
        except:
            print("Invalid Argument given.")
            sys.exit(1)
        self.mode=self.get_mode()
        self.path = os.path.dirname(os.path.abspath(__file__))
        self.thresholds=self.get_thresholds()
        self.domainfilter=self.get_domain_filter()
        self.projectfilter=self.get_project_filter()
        self.cache=self.get_cache()
        self.cs=self.connect_to_cs()

        if self.mode == None:
            print("No check selected")
            sys.exit(1)
        self.checks={
                'capacity':self.check_capacity,
                'virtualrouter':self.check_virtualrouter,
                'systemvm':self.check_systemvm,
                'hoststatus':self.check_hv_status,
                'vmplacement':self.check_vm_placement,
                'projects':self.check_project_status,
                'domains': self.check_domain_status,
                'offerings':self.check_offerings
                }

    def run(self):
        if self.mode not in self.checks:
            print("Check not found")
            sys.exit(1)
        function=self.checks[self.mode]
        function()

    def get_thresholds(self):
        file=None
        for option, value in self.myopts:
            if option == "-f":
                file=value

        if file is  None:
            return {}

        try:
            f = open(file, "r")
            output = json.loads(f.read())
            f.close
        except:
            output = {}
        return output

    def get_mode(self):
        for option, value in self.myopts:
            if option == "-m":
                return value

    def get_domain_filter(self):
        for option, value in self.myopts:
            if option == "-d":
                return value

    def get_project_filter(self):
        for option, value in self.myopts:
            if option == "-p":
                return value

    def create_output(self,message,performance_data,exitcode):
        for option, value in self.myopts:
            if option == "-c":
                #Check with Cache output
                if self.cache == message:
                    exitcode=0
                else:
                    self.set_cache(message)

        chars=["-","."]
        message=message + "|"
        for data in performance_data:
            first=0
            for value in data:
                if first == 0:
                    for char in chars:
                        value=value.replace(char,"_")
                    first=1
                    tempdata=value + "="
                else:
                    tempdata = tempdata + str(value) + ";"
            message=message + " " + tempdata
        print(message)
        sys.exit(exitcode)

    def set_cache(self,output):
        f = open(self.path + "/cache/"+self.mode,"w")
        f.write(output)
        f.close

    def get_cache(self):
        try:
            f = open(self.path+"/cache/"+self.mode,"r")
            output = f.read()
            f.close
        except:
            output=""
        return output

    def connect_to_cs(self):
        tempdict={}
        #Read config
        try:
            f=open(self.path+"/config","r")
            config=f.readlines()
        except:
            print("Somethings wrong with your config file")
            sys.exit(2)

        for entry in config:
            entry=entry.replace("\n","")
            temarray=entry.split("=")
            tempdict[temarray[0]]=temarray[1]

        if tempdict['verify'] is None:
            tempdict['verify']=False

        cs = CloudStack(
                        endpoint=tempdict['endpoint'],
                        key=tempdict['key'],
                        secret=tempdict['secret'],
                        verify=tempdict['verify']
                        )
        return cs

    ############################
    #### Check definitions #####
    ############################

    def check_capacity(self):

        message="See long output: \n<pre>\n"
        exitcode=0
        performancedata=[]

        types={
            0:'CAPACITY_TYPE_MEMORY',
            1:'CAPACITY_TYPE_CPU',
            2:'CAPACITY_TYPE_STORAGE',
            3:'CAPACITY_TYPE_STORAGE_ALLOCATED',
            4:'CAPACITY_TYPE_VIRTUAL_NETWORK_PUBLIC_IP',
            5:'CAPACITY_TYPE_PRIVATE_IP',
            6:'CAPACITY_TYPE_SECONDARY_STORAGE',
            7:'CAPACITY_TYPE_VLAN',
            8:'CAPACITY_TYPE_DIRECT_ATTACHED_PUBLIC_IP',
            19:'CAPACITY_TYPE_LOCAL_STORAGE',}

        resources=self.cs.listCapacity()
        for resource in resources['capacity']:
            name=types[resource['type']]
            warn=0
            critical=0
            if name in self.thresholds['thresholds']:
                warn=self.thresholds['thresholds'][name]['warn']
                critical=self.thresholds['thresholds'][name]['critical']
                if resource['percentused'] > warn and resource['percentused'] < critical:
                    message=message + "WARN:     {:40} has reached warning value. Threshold:{}% Value:{}%\n".format(name,warn,resource['percentused'])
                    if exitcode < 1:
                        exitcode=1
                elif resource['percentused'] > critical:
                    message=message + "Critical: {:40} has reached warning value. Threshold:{}% Value:{}%\n".format(name,warn,resource['percentused'])
                    if exitcode < 2:
                        exitcode=2
                else:
                    message = message + "OK:       {:40} is in status ok. Value:{}% \n".format(name,resource['percentused'])
            else:
                message = message + "OK:       {:40} No Thresholds given. Value:{}%\n".format(name,resource['percentused'])

            #Add Performance data
            performancedata.append((name, resource['percentused']+"%",warn,critical,'' ))

        message += "</pre>\n"
        self.create_output(message,performancedata,exitcode)



    def check_virtualrouter(self):

        message="See long output: \n<pre>Name       Status   Running    Upgrade\n"
        vpcmessage="Status of redundant VPC Routers\nName    Status        Status\n"
        exitcode=0
        performancedata=[]
        vpcdict = {}
        routerlist=[]
        shutdownrouters=0
        updaterouters=0

        domains=self.cs.listDomains()
        for domain in domains['domain']:
            projects=self.cs.listProjects(domainid=domain["id"])
            if "project" in projects:
                for project in projects["project"]:
                    routers = self.cs.listRouters(projectid=project["id"])
                    if "router" in routers:
                        for router in routers["router"]:
                            routerlist.append(router)
            routers=self.cs.listRouters(domainid=domain["id"])
            if "router" in routers:
                for router in routers["router"]:
                    routerlist.append(router)

        for router in routerlist:
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
        self.create_output(message,performancedata,exitcode)

    def check_systemvm(self):

        message="See long output: \n<pre>"
        exitcode=0
        shutdownvms=0
        performancedata=[]

        sysvms=self.cs.listSystemVms()
        for vm in sysvms["systemvm"]:
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
        self.create_output(message,performancedata,exitcode)

    def check_project_status(self):

        message="See long output: \n<pre>"
        exitcode=0
        projects=[]
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

        domains = self.cs.listDomains(id=self.domainfilter)['domain']
        if self.projectfilter is not None and self.domainfilter is not None:
            temp = self.cs.listProjects(domainid=self.domainfilter,id=self.projectfilter)
            if 'project' in temp:
                projects += temp['project']
        else:
            for domain in domains:
                temp = self.cs.listProjects(domainid=domain['id'])
                if 'project' in temp:
                    projects = temp['project']

                    for project in projects:
                        message+="\nResults for Project "+ project['name'] +":"
                        for value in  values:
                            warn = None
                            crit = None
                            if project[value+'limit'] != "Unlimited" \
                            and project[value+'limit'] != "0" \
                            and project[value+'total'] != "Unlimited":
                                percentvalue = (int(project[value+'total'])/int(project[value+'limit']))*100
                                if "thresholds" in self.thresholds:
                                    identifier=domain['name']+"-"+project['name']
                                    if identifier in self.thresholds['thresholds']:
                                        if value in self.thresholds['thresholds'][project['name']]:
                                            warn = self.thresholds['thresholds'][project['name']][value]['warn']
                                            crit = self.thresholds['thresholds'][project['name']][value]['critical']
                                    else:
                                        if "global" in self.thresholds:
                                            if value in self.thresholds['global']:
                                                warn = self.thresholds['global'][value]['warn']
                                                crit = self.thresholds['global'][value]['critical']

                                if warn != None and crit != None:
                                    if int(warn) < percentvalue and int(crit) > percentvalue:
                                        message += "\n--> Warning: Project " + str(project['name']) + " has reached threshold for " + value + ": " + str(percentvalue)
                                        exitcode = 1
                                    elif int(crit) < percentvalue:
                                        message += "\n--> Critical: Project " + str(project['name']) + " has reached threshold for " + value + ": " + str(percentvalue)
                                        exitcode = 2

                                performancedata.append((domain['name']+"+"+project['name']+"+usage" + "!" + value, percentvalue, '', '', ''))
                                performancedata.append((domain['name'] + "+" + project['name'] + "+total" + "!" + value,project[value+'total'], '', '', ''))
                            else:
                                if project[value+'total'] != "Unlimited":
                                    performancedata.append((domain['name'] + "+" + project['name'] + "+total" + "!" + value,project[value + 'total'], '', '', ''))
                                else:
                                    performancedata.append((domain['name'] + "+" + project['name'] + "+total" + "!" + value,-1, '', '', ''))

                                performancedata.append((domain['name']+"+" + project['name'] + "+usage" + "!" + value, -1, '', '', ''))

        message += "</pre>\n"
        self.create_output(message,performancedata,exitcode)

    def check_domain_status(self):

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

        domains = self.cs.listDomains(id=self.domainfilter)
        for domain in domains['domain']:
            message+="\nResults for Domain "+ domain['name'] +":"
            for value in  values:
                warn=None
                crit=None
                if domain[value+'limit'] != "Unlimited" \
                and domain[value+'limit'] != "0" \
                and domain[value+'total'] != "Unlimited":
                    percentvalue = (int(domain[value+'total'])/int(domain[value+'limit']))*100
                    if "thresholds" in self.thresholds:
                        if domain['name'] in self.thresholds['thresholds']:
                            if value in self.thresholds['thresholds'][domain['name']]:
                                warn=self.thresholds['thresholds'][domain['name']][value]['warn']
                                crit=self.thresholds['thresholds'][domain['name']][value]['critical']
                    else:
                        if "global" in self.thresholds:
                            if value in self.thresholds['global'] and domain[value] != "Unlimited":
                                warn=self.thresholds['global'][value]['warn']
                                crit=self.thresholds['global'][value]['critical']

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
        self.create_output(message,performancedata,exitcode)

    def check_hv_status(self):

        message="See long output: \n<pre>\n"
        exitcode=0
        shutdownhosts={}
        disabledhosts={}
        performancedata=[]
        lastcluster=""

        hosts=self.cs.listHosts(type="Routing")

        for host in sorted(hosts["host"],key=lambda x: x['clustername']):
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
        self.create_output(message,performancedata,exitcode)

    def check_vm_placement(self):

        offerings = self.cs.listServiceOfferings()
        clusters = self.cs.listClusters()
        olddistribution = {}
        newdistribution = {}
        oldcpu = 0
        oldmem = 0
        newcpu = 0
        newmem = 0
        performancedata=[]
        offeringdict_old = {}
        offeringdict_new = {}
        migration_possible=0
        message="See long output: \n<pre>"


        for cluster in clusters['cluster']:
            clustername = cluster['name']
            hvstatus=self.get_hvstructure(cluster)

            #Copy the original status
            hvcopy = copy.deepcopy(hvstatus)
            #Create list for excepted hvs
            hvexepted = {}

            #Rate HVs with CPU Memory and CPU*MEM Ratio and migrate VMs
            message +="\n"
            message +="Possible Migrations in Cluster:" + clustername + "\n"
            for i in range(0, len(hvcopy) - 1):
                hvranking=self.hv_ranking(hvcopy,hvexepted)
                #Get most empty HV from List
                if len(hvranking) > 0:
                    besthv = hvranking[0]
                #Copy sorted list of VMs from Besthv
                tmpvms = self.sort_objects(copy.deepcopy(besthv['vms']),"cpu","mem")
                #Add HV to Excepted List (This is ugly please fix)
                hvexepted[besthv['name']] = ""

                #Migrate all VMs from HV to another Host
                for vmid in range(0,len(tmpvms)):
                    vm = tmpvms[vmid]
                    #tempranking = hv_ranking(hvcopy, {})
                    for hv in reversed(hvranking):
                        if hv['name'] not in hvexepted:
                            if vm['cpu'] <= hv['cpufree'] and vm['mem'] <= hv['memfree']:
                                migration_possible=1
                                besthv['cpufree'] += vm['cpu']
                                besthv['memfree'] += vm['mem']
                                hv['vms'].append(vm)
                                hv['cpufree'] -= vm['cpu']
                                hv['memfree'] -= vm['mem']
                                delvm = None
                                for counter in range(0, len(besthv['vms'])):
                                    if vm['name'] == besthv['vms'][counter]['name']:
                                        delvm = counter
                                del besthv['vms'][delvm]
                                message+="Migrate " + vm['name'] + "(" + vm['instance'] + ")" + " from " + besthv['name'] + " to " + hv['name'] + "\n"
                                break

            # Deploy offerings on old and new HV schema
            hvstatus_temp = copy.deepcopy(hvstatus)
            hvcopy_temp = copy.deepcopy(hvcopy)
            for offering in self.sort_objects(offerings['serviceoffering'],"cpunumber","memory"):
                #Except our Zero Offering
                if offering['name'] == "Zero":
                    del(offering)
                    continue
                if offering['iscustomized'] is False:

                    #Deploy on original HVs
                    (hvstatus,tempdistribution,tempmem,tempcpu) = self.deploy_offerings(offering, hvstatus)
                    oldmem+=tempmem
                    oldcpu+=tempcpu
                    olddistribution[offering['name']] = tempdistribution[offering['name']]

                    #Deploy on optimized HVs
                    (hvcopy, tempdistribution, tempmem, tempcpu) = self.deploy_offerings(offering, hvcopy)
                    newmem+=tempmem
                    newcpu+=tempcpu
                    newdistribution[offering['name']]=tempdistribution[offering['name']]

                    #Get absolut distribution from old constelation
                    (temp, tempdistribution, tempmem, tempcpu) = self.deploy_offerings(offering, hvstatus_temp)
                    if offering['name'] not in offeringdict_old:
                        offeringdict_old[offering['name']]=0
                    offeringdict_old[offering['name']]+=tempdistribution[offering['name']]

                    # Get absolut distribution from new constelation
                    (temp, tempdistribution, tempmem, tempcpu) = self.deploy_offerings(offering, hvcopy_temp)
                    if offering['name'] not in offeringdict_new:
                        offeringdict_new[offering['name']]=0
                    offeringdict_new[offering['name']]+=tempdistribution[offering['name']]


            headerline="! OLD! NEW!DIFF!          !\n"
            for offering in sorted(olddistribution.keys()):
                headerline+="!{:4}!{:4}!{:4}!{:10}!\n".format(olddistribution[offering],newdistribution[offering],newdistribution[offering] - olddistribution[offering],offering)
                performancedata.append((clustername+"-"+offering +"-Cascading-Diff", (newdistribution[offering] - olddistribution[offering]), '', '', ''))


            message +="\n"
            message +="Cascading Distribution of offerings before and after in Cluster:" + clustername + "\n"
            message +=headerline+"\n"

            message +=""+"\n"
            message +="Usage diffrence from old deployment in Cluster:" + clustername + "\n"
            cpudiff=(newcpu / 2000) - (oldcpu / 2000)
            memdiff=(newmem / 1024 / 1024) - (oldmem / 1024 / 1024)
            message +="CPU: "+str(cpudiff)+"\n"
            message +="MEM: "+str(memdiff)+"\n"
            message +="-----------------------------------------------------------------------\n"

            performancedata.append((clustername+"_CPU_Usage_Diff",cpudiff, '', '', ''))
            performancedata.append((clustername+"_MEM_Usage_Diff",memdiff, '', '', ''))

            headerline2 = "\n!  Offering!   Old!   New!  Diff!\n"
            for offering in sorted(offeringdict_old.keys()):
                headerline2+="!{:10}!{:6}!{:6}!{:6}!\n".format(offering,offeringdict_old[offering],offeringdict_new[offering],(offeringdict_new[offering]-offeringdict_old[offering]))
                performancedata.append((clustername+"-"+offering+"-Absolut-Diff",(offeringdict_new[offering]-offeringdict_old[offering]), '', '', ''))

            message +="\n"
            message +="Absolut Distribution of offerings before and after in Cluster:" + clustername + "\n"
            message +=headerline2+"\n"
            message += "-----------------------------------------------------------------------\n"

            if migration_possible == 1:
                exitcode=1
            else:
                exitcode=0

        message += "</pre>\n"
        self.create_output(message,performancedata,exitcode)

    def check_offerings(self):

        offerings = self.cs.listServiceOfferings()
        clusters = self.cs.listClusters()
        offeringdict={}
        errors=""
        performancedata=[]
        message="See long output: \n<pre>"

        for cluster in clusters['cluster']:
            clustername = cluster['name']
            hvstatus=self.get_hvstructure(cluster,withvm=0)
            for offering in self.sort_objects(offerings['serviceoffering'], "cpunumber", "memory"):
                if offering['iscustomized'] is False:
                    (temphvstatus, tempdistribution, tempmem, tempcpu)=self.deploy_offerings(offering, hvstatus)
                    if offering['name'] not in offeringdict:
                        offeringdict[offering['name']]=0
                    offeringdict[offering['name']]+=tempdistribution[offering['name']]

            header = "\n!  Offering! Count!\n"
            for offering in sorted(offeringdict.keys()):
                if offering in self.thresholds:
                    warn = self.thresholds[offering]['warn']
                    critical = self.thresholds[offering]['critical']
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
        self.create_output(message,performancedata,exitcode)


    def sort_objects(self,array,cpuvalue,memvalue):

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

    def hv_ranking(self,hvcopy,hvexepted):
        for i in range(0, len(hvcopy) - 1):
            hvranking = []
            for hv in hvcopy:
                rankingposition = len(hvranking)
                if hv['name'] not in hvexepted.keys():
                    if hv['cpufree'] <= 0:
                        hv['ratio'] = 0
                    else:
                        hv['ratio'] = hv['memfree'] * hv['cpufree']
                    if hvranking is None:
                        hvranking.insert(0, hv)
                    else:
                        for i in hvranking:
                            if hv['cpufree'] >= i['cpufree'] and hv['memfree'] >= i['memfree']:
                                rankingposition -= 1
                            elif hv['cpufree'] >= i['cpufree'] and hv['memfree'] <= i['memfree'] and hv['ratio'] >= i[
                                'ratio']:
                                rankingposition -= 1
                            elif hv['cpufree'] <= i['cpufree'] and hv['memfree'] >= i['memfree'] and hv['ratio'] >= i[
                                'ratio']:
                                rankingposition -= 1
                    hvranking.insert(rankingposition, hv)
        return hvranking

    def deploy_offerings(self,offering,hvorig):

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


    def get_hvstructure(self,cluster,withvm=1):

        hvstatus = []
        domains = self.cs.listDomains()
        vmdict = []
        memthreshold=cluster['resourcedetails']['cluster.memory.allocated.capacity.disablethreshold']
        memovercommit=cluster['resourcedetails']['memoryOvercommitRatio']
        cputhreshold = cluster['resourcedetails']['cluster.cpu.allocated.capacity.disablethreshold']
        cpuovercommit = cluster['resourcedetails']['cpuOvercommitRatio']
        clusterid=cluster['id']

        hosts = self.cs.listHosts(clusterid=clusterid)

        #Get Host list
        for host in hosts['host']:
            if host['type'] == "Routing":
                hvstatus.append({
                    'name': host['name'],
                    'cpu': (float(host['cpunumber'] * host['cpuspeed']) * float(cpuovercommit)) * float(cputhreshold),
                    'mem': ((host['memorytotal'] * float(memovercommit)) * float(memthreshold) ) / 1024,
                    'memfree': ((host['memorytotal'] * float(memthreshold)) - host['memoryused']) / 1024,
                    'cpufree': ((float(host['cpunumber'] * host['cpuspeed']) * float(cpuovercommit)) * float(cputhreshold)) - (float(host['cpuallocated'].replace("%", "")) * ((host['cpunumber'] * host['cpuspeed']) / 100)),
                    'ratio': None,
                    'vms': [],
                })

        if withvm == 1:
            # Get VM list
            for domain in domains['domain']:
                projects = self.cs.listProjects(domainid=domain['id'])
                if "project" in projects.keys():
                    for project in projects['project']:
                        vms = self.cs.listVirtualMachines(projectid=project['id'])
                        for vm in vms['virtualmachine']:
                            vmdict.append(vm)

            #Add VMs to their Hypervisors
            for vm in vmdict:
                for hv in hvstatus:
                    if "hostname" in vm:
                        if vm['hostname'] == hv['name']:
                            hv['vms'].append({
                                'name': vm['name'],
                                'cpu': vm['cpunumber'] * vm['cpuspeed'],
                                'mem': vm['memory']*1024,
                                'instance': vm['instancename'],
                            })
        return hvstatus

#########################
#### The Main script ####
#########################
newcheck=check_cs()
newcheck.run()