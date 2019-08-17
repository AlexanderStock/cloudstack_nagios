from cs import CloudStack
import sys, os

class csresources:

    def __init__(self):
        tempdict = {}
        path = os.path.dirname(os.path.abspath(__file__))
        # Read config
        try:
            f = open(path + "/../cloudstack.config", "r")
            config = f.readlines()
        except:
            print("Somethings wrong with your config file")
            sys.exit(2)

        for entry in config:
            entry = entry.replace("\n", "")
            temarray = entry.split("=")
            tempdict[temarray[0]] = temarray[1]

        if tempdict['verify'] is None:
            tempdict['verify'] = False

        self.cs = CloudStack(
            endpoint=tempdict['endpoint'],
            key=tempdict['key'],
            secret=tempdict['secret'],
            verify=False
        )


    def list_virtual_routers(self):
        routerList = []
        domains = self.cs.listDomains()
        for domain in domains['domain']:
            projects = self.cs.listProjects(domainid=domain["id"])
            if "project" in projects:
                for project in projects["project"]:
                    routers = self.cs.listRouters(projectid=project["id"])
                    if "router" in routers:
                        for router in routers["router"]:
                            routerList.append(router)
            routers = self.cs.listRouters(domainid=domain["id"])
            if "router" in routers:
                for router in routers["router"]:
                    routerList.append(router)
        return routerList

    def list_system_vms(self):
        return self.cs.listSystemVms()['systemvm']

    def list_capacity(self):
        return self.cs.listCapacity()['capacity']

    def list_projects(self,domainfilter=None,projectfilter=None):
        projects = []
        domains = self.cs.listDomains(id=domainfilter)['domain']
        if projectfilter is not None and domainfilter is not None:
            temp = self.cs.listProjects(domainid=domainfilter,id=projectfilter)
            if 'project' in temp:
                projects += temp['project']
        else:
            for domain in domains:
                temp = self.cs.listProjects(domainid=domain['id'])
                if 'project' in temp:
                    for project in temp['project']:
                        projects.append(project)
        return projects

    def list_domains(self,domainfilter=None):
        return self.cs.listDomains(id=domainfilter)['domain']

    def list_clusters(self):
        return self.cs.listClusters()['cluster']

    def list_offerings(self):
        return self.cs.listServiceOfferings()['serviceoffering']

    def list_hvs(self):
        return self.cs.listHosts(type="Routing")['host']

    def get_hvstructure(self,cluster,withvm=1):
        hvstatus = []
        domains = self.cs.listDomains()
        vmdict = []
        if 'cluster.memory.allocated.capacity.disablethreshold' in cluster['resourcedetails']:
            memthreshold= cluster['resourcedetails']['cluster.memory.allocated.capacity.disablethreshold']
        else:
            memthreshold = 1
        if 'cluster.cpu.allocated.capacity.disablethreshold' in cluster['resourcedetails']:
            cputhreshold = cluster['resourcedetails']['cluster.cpu.allocated.capacity.disablethreshold']
        else:
            cputhreshold = 1
        memovercommit= cluster['resourcedetails']['memoryOvercommitRatio']
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


        ##Split this as an extra function!!!!!!
        if withvm == 1:
            # Get VM list
            for domain in domains['domain']:
                projects = self.cs.listProjects(domainid=domain['id'])
                if "project" in projects.keys():
                    for project in projects['project']:
                        vms = self.cs.listVirtualMachines(projectid=project['id'])
                        if "virtualmachine" in vms:
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