# Get AP name populate a file with accesspoint names and run command file.
from netmiko import ConnectHandler
from SOD_WLC_CREDS import *
import textfsm
import logging
import sys

# logging.basicConfig(filename='netmiko.log', level=logging.DEBUG)
# logger = logging.getLogger("netmiko")

reload(sys)
sys.setdefaultencoding('utf8')

"""prepare file and open log """

orig_stdout = sys.stdout
f = open('AP-CHANGE-PRIM-SEC', 'w')
sys.stdout = f

"""TEXTFSM lines of code used for filtering accesspoint names
"""

temlate = open('ap-template')    # File to be used for accesspoints
re_table = textfsm.TextFSM(temlate)             # Run textFSM on template file
net_connect = ConnectHandler(**cisco_wlc4)      # Connect to specific device
c = net_connect.send_command('sho ap summary')  # Send command needed to device
fsm_results = re_table.ParseText(c)             # Parse output and store as a tuple

"""For loop iterating over the results from matching TextFSM
"""

for shutdown in fsm_results:
    for item in shutdown:
        print('config ap primary-base WLC_8-1'),(item),('172.16.252.12')
x = net_connect.disconnect

for command_to in fsm_results:
    for item in command_to:
        print('config ap secondary-base WLC_9-1'),(item),('172.16.252.13')
x = net_connect.disconnect

for turnon in fsm_results:
    for item in turnon:
        print('config ap reset'),(item)
        print('y')
x = net_connect.disconnect

sys.stdout = orig_stdout
f.close()       # Close file so we can use it in code below
for execute in fsm_results:
    for item in execute:
        net_connect = ConnectHandler(**cisco_wlc4)      # Connect to specific device
        c = net_connect.send_config_from_file('AP-CHANGE-PRIM-SEC')  # Send command needed to device
        print(c)
        c = net_connect.disconnect()
