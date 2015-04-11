#import pdb
import glob
import csv
import re

from jinja2 import Template
from pprint import pprint as pp
#from jnpr.junos import Device

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


topology = load_switches()
#pp(topology)

target = find_switch("PE3714080640", topology)
#pp(target)

with open("access_switch.j2") as t_fh:
    t_format = t_fh.read()

template = Template(t_format)
print(template.render(target))

