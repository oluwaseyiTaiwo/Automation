######
# oluwaseyimosobalaje.taiwo@gmail.com
######
# AUTOMATION Supports for Pulling _NOKIA AND ZTE ROUTER NAMES
######

import pandas as pd
import netmiko
from netmiko import ConnectHandler
from ntc_templates.parse import parse_output
from datetime import datetime
import concurrent.futures
import time
import re
t1 = time.perf_counter()
print("Remote_Ping_Test_Start Time",
      datetime.now().strftime("%d/%m/%y %I:%M:%S %p"))


SITE_NAME = []
SITE_IP = []
System_Name_LIST = []
Status_1 = []
type_11 = []
ip_list = (input("Drag and drop Document with IP's:")).strip('"')
file = pd.read_csv(ip_list)
nodenum = 0


def nokia(ip_address, node_name, connection):
    global SITE_NAME, SITE_IP, System_Name_LIST, Status_1, node_ip_list1, node1_name_list1, Status, nodenum, type_11
    interfaces = (connection.send_command_timing("show system information"))
    System_Name = re.compile(r"System Name[ \t]{2,}: (?P<System_Name>.*)")
    System_Name_match = System_Name.finditer(interfaces)
    list_1 = []
    for x in System_Name_match:
        list_1.append(x.groupdict())
    SITE_NAME.append(f'{node_name}')
    SITE_IP.append(f'{ip_address}')
    System_Name_LIST.append(f'{list_1[0]["System_Name"]}')
    Status_1.append("Online")
    type_11.append("NOKIA")
    connection.disconnect()


def zte(ip_address, node_name, connection):
    global SITE_NAME, SITE_IP, System_Name_LIST, Status_1, node_ip_list1, node1_name_list1, Status, nodenum, type_11
    interfaces = (connection.send_command_timing("show hostname"))
    SITE_NAME.append(f'{node_name}')
    SITE_IP.append(f'{ip_address}')
    System_Name_LIST.append(f'{interfaces}')
    Status_1.append("Online")
    type_11.append("ZTE")
    connection.disconnect()


def main(ip_address, node_name):
    global nodenum, SITE_NAME, SITE_IP, System_Name_LIST, Status_1, node_ip_list1, node1_name_list1, Status, type_11
    nodenum += 1
    try:
        try:
            try:
                print(nodenum, "Connecting with Nokia SSH to", node_name)
                connection = netmiko.ConnectHandler(
                    ip=ip_address, device_type="nokia_sros", username="admin", password="Ng12345!")
                print("Connected using SSH to", node_name)
                nokia(ip_address, node_name, connection)
            except:
                print(nodenum, "Connecting with Nokia Telnet to", node_name)
                connection = netmiko.ConnectHandler(
                    ip=ip_address, device_type="nokia_sros_telnet", username="admin", password="Ng12345!")
                print("Connected using Telnet to", node_name)
                nokia(ip_address, node_name, connection)
        except:
            try:
                print(nodenum, "Connecting with ZTE SSH to", node_name)
                connection = netmiko.ConnectHandler(
                    ip=ip_address, device_type="zte_zxros", username="Seyi", password="Seyi@321126")
                print("Connected using SSH to", node_name)
                zte(ip_address, node_name, connection)
            except:
                print(nodenum, "Connecting with ZTE Telnet to", node_name)
                connection = netmiko.ConnectHandler(
                    ip=ip_address, device_type="zte_zxros_telnet", username="Seyi", password="Seyi@321126")
                print("Connected using Telnet to", node_name)
                zte(ip_address, node_name, connection)
    except:
        SITE_NAME.append(node_name)
        SITE_IP.append(ip_address)
        System_Name_LIST.append("unknown")
        Status_1.append("Offline")
        type_11.append("unknown")


with concurrent.futures.ThreadPoolExecutor(max_workers=100) as exector:
    for x in range(file.shape[0]):
        exector.submit(
            main, ip_address=file['Site ID'][x], node_name=file['Name'][x])

now_time = datetime.now().strftime("%d_%m_%y")
now_time_NF = datetime.now().strftime("%I_%M_%S %p")
# CREATING AND NAMING FILE
df_out_2 = pd.DataFrame(list(zip(SITE_IP, SITE_NAME, Status_1, type_11, System_Name_LIST)), columns=[
                        'IP Address', 'Router Name', "Status", "Type", "Actual-Name"])
df_out_2.to_excel(
    f'Router_Name_Date_({now_time})__ Time_({now_time_NF}).xlsx', index=False)
# CREATING AND NAMING FILE
print(
    f"Router_Name_Date_({now_time})__ Time_({now_time_NF}).xlsx created \n Find it to see output")
print("End Time", datetime.now().strftime("%d/%m/%y %I:%M:%S %p"))
print("Router_Name Completed")
t2 = time.perf_counter()
print(f"Finished in {round(t2-t1,2)} Second(s)")
