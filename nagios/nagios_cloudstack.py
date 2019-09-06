#!/usr/bin/python
# by Alexander Stock
import getopt
import sys
import os
import json
from lib.cschecks import *
from lib.csresources import csresources


class check_cs():

    def __init__(self):
        try:
            self.myopts, self.args = getopt.getopt(sys.argv[1:], "f:m:d:p:c")
        except:
            print("Invalid Argument given.")
            sys.exit(1)
        self.mode = self.get_mode()
        self.path = os.path.dirname(os.path.abspath(__file__))
        self.thresholds = self.get_thresholds()
        self.domainfilter = self.get_domain_filter()
        self.projectfilter = self.get_project_filter()
        self.cache = self.get_cache()
        self.csr = csresources()

        if self.mode == None:
            print("No check selected")
            sys.exit(1)
        self.checks = {
                'capacity':{'check':check_capacity,'data':self.csr.list_capacity},
                'virtualrouter':{'check':check_virtualrouter,'data':self.csr.list_virtual_routers},
                'systemvm':{'check':check_systemvm,'data':self.csr.list_system_vms},
                'hoststatus':{'check':check_hvstatus,'data':self.csr.list_hvs},
                'projects':{'check':check_projects,'data':self.csr.list_projects},
                'domains':{'check':check_domains,'data':self.csr.list_domains},
                'offerings':{'check':check_offerings,'data':self.csr.list_offerings},
                }

    def run(self):
        if self.mode not in self.checks:
            print("Check not found")
            sys.exit(1)
        checkFunction = self.checks[self.mode]['check']
        dataFunction = self.checks[self.mode]['data']
        self.create_output(checkFunction(metric=dataFunction(),thresholds={}))

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
            f.close()
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

    def set_cache(self,output):
        f = open(self.path + "/cache/"+self.mode,"w")
        f.write(output)
        f.close()

    def get_cache(self):
        try:
            f = open(self.path+"/cache/"+self.mode,"r")
            output = f.read()
            f.close()
        except:
            output=""
        return output

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


#########################
#### The Main script ####
#########################
newcheck=check_cs()
newcheck.run()