#import pdb
import glob
import csv
import re

from jinja2 import Template
from pprint import pprint as pp

from jnpr.junos import Device
from jnpr.junos.utils.config import Config

HOST_CSV_DIR = "./hostcsv"
PORT_REGEX = re.compile(r"^([g,x]e)")

def load_switches():
    # Create initial place holder for all discovered switches
    all_switches = []

    for files in glob.glob("{0}/*.csv".format(HOST_CSV_DIR) ):
        # print files 
        lines = csv.reader(open(files,"rU"))
        
        # Create data structure for individual switches
        new_switch = {
            'hostname': "Unknown",
            'interfaces': []
        }

        for line in lines:
            if line[0] == "Serial Number":
                #print "Skip Header"
                next_line = lines.next()
                new_switch['serial_number'] = next_line[0]
                new_switch['hostname'] = next_line[1]
                new_switch['mgmt_ip'] = next_line[2]
                next

            if line[0] == "":
                #print "Skip Blanks"
                next

            elif PORT_REGEX.match(line[0]):
                new_interface = {
                    'name': line[0],
                    'vlan': line[1],
                    'mode': line[2],
                    'description': line[3]
                }

                new_switch['interfaces'].append(new_interface)

        all_switches.append(new_switch)
    return all_switches

def find_switch(sn, switch_list):
    for switch in switch_list:
        if switch['serial_number'] == sn:
            return switch
    return False

def customize(hostip, switchvars, templatefile="access_switch.j2"):
    dev = Device(user="netconf-test", host=hostip, password="lab123")
    dev.open()
 
    dev.bind(cu=Config)
    dev.cu
    print "Loading template onto: {0} (SN: {1}) @ {2}".format(switchvars['hostname'], switchvars['serial_number'], switchvars['mgmt_ip'])

    dev.cu.load(template_path=templatefile, template_vars=switchvars, format="set")
    dev.cu.commit()
    dev.close()

def load_ztp_hosts():
    lines = csv.reader(open("./ztp-hosts.csv","rU"))
    ztp_switches = []
    # Create data structure for individual switches

    for line in lines:
        new_switch = {
            'ztp_ip': line[0],
            'hostname': line[1],
            'model': line[2],
            'serial_number': line[3],
            'version': line[4],
        }
        ztp_switches.append(new_switch)
    return ztp_switches

#########
#########
#########

print "Building known topology..."
topology = load_switches()

print "Building discovered hosts..."
ztp_hosts = load_ztp_hosts()

print "Begin customizing hosts..."
for host in ztp_hosts:
    target = find_switch(host['serial_number'], topology)
    customize(host['ztp_ip'], target)
