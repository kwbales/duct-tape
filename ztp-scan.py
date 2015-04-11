import pdb
import subprocess

from jnpr.junos import Device

#################################
# Variables required for access #
#################################

MGMT_subnet = "172.32.32"
host_ip = range(180,184)
username = 'netconf-test'
password = 'lab123'


def ping(host):
    result = subprocess.call(["ping","-n","-c","1","-t","1","-w","1",host],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    if result == 0:
        return True
    else:
        return False

for ip in host_ip:
    host = "%s.%s" % (MGMT_subnet, ip)
    if ping(host):
        try:
            dev = Device( user=username, host=host, password=password, auto_probe=1 ).open()
            #pdb.set_trace()
            print "%s,%s,%s,%s,%s" % (host, dev.facts['hostname'], dev.facts['model'], dev.facts['serialnumber'], dev.facts['version'] )
        except:
            next