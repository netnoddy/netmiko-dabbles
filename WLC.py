from netmiko import ConnectHandler
from SOD_WLC_CREDS import *
import sys
from datetime import date
import textfsm
import logging
# logging.basicConfig(filename='netmiko.log', level=logging.DEBUG)
# logger = logging.getLogger("netmiko")

"""prepare file and open log
"""
reload(sys)
sys.setdefaultencoding('utf8')
orig_stdout = sys.stdout

filename ='APLOG_WLC_{}.txt'.format(date.today())
f = open(filename, 'a')
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

for command_to in fsm_results:
    for item in command_to:
        cmd = 'show ap config general {}'.format(item)
        r = net_connect.send_command(cmd)
        print(cmd)
        print(r)

sys.stdout = orig_stdout
f.close()
