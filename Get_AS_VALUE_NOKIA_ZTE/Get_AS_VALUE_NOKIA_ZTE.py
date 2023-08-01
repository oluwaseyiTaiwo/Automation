######
# oluwaseyimosobalaje.taiwo@gmail.com
######
# AUTOMATION Support for Get_AS_VALUE_OF_Nokia and ZTE routers
######
######
import pandas as pd
import netmiko
from netmiko import ConnectHandler
import csv
from ntc_templates.parse import parse_output
from datetime import datetime
import time
import concurrent.futures
import re


t1 = time.perf_counter()
print("Start Time", datetime.now().strftime("%d/%m/%y %I:%M:%S %p"))

ip_list = input("Drag and drop Document with IP's:")
file = pd.read_csv(ip_list)

status = []
node1_name = []
node_ip = []
as_number = []
type_router = []
nodenum = 0


now_date1_NF = datetime.now().strftime("%d_%m_%y")
now_time1_NF = datetime.now().strftime("%I_%M_%S %p")


def main_2(ip_address, node_name, connection):
    global status, node1_name, node_ip, nodenum, as_number, type_router
    print('Connection successful, fetching the output...')
    print("login to " + node_name + " was successful")
    As_number_output = (connection.send_command_timing(
        "show router bgp neighbor | match AS"))
    As_number = re.compile(r"Local[ \t]{1,}AS[ \t]{2,}:[ \t]{1,}(?P<AS>\S+)")
    As_number_match = As_number.finditer(As_number_output)
    list_1 = []
    for x in As_number_match:
        list_1.append(x.groupdict())
    as_number.append(list_1[0]["AS"])
    type_router.append("Nokia")
    status.append('online')
    node1_name.append(f'{node_name}')
    node_ip.append(f'{ip_address}')
    print("Done with ", node_name)


def zte(ip_address, node_name, connection):
    global status, node1_name, node_ip, nodenum, as_number, type_router
    print('Connection successful, fetching the output...')
    print("login to " + node_name + " was successful")
    As_number_output = (connection.send_command_timing(
        "show running-config bgp"))
    As_number = re.compile(r"router\s+bgp\s+(?P<AS>.*)")
    As_number_match = As_number.finditer(As_number_output)
    list_1 = []
    for x in As_number_match:
        list_1.append(x.groupdict())
    type_router.append("ZTE")
    as_number.append(list_1[0]["AS"])
    status.append('online')
    node1_name.append(f'{node_name}')
    node_ip.append(f'{ip_address}')
    print("Done with ", node_name)


def main(ip_address, node_name):
    global status, node1_name, node_ip, nodenum
    nodenum += 1
    try:
        try:
            try:
                print('Node', nodenum, "...checking IP Address with SSH",
                      ip_address, node_name)
                connection = netmiko.ConnectHandler(
                    ip=ip_address, device_type="nokia_sros", username="xxxx", password="xxx!", timeout=60)
                main_2(ip_address, node_name, connection)
                connection.disconnect()
            except:
                print('Node', nodenum, "...checking IP Address with TELNET",
                      ip_address, node_name)
                connection = netmiko.ConnectHandler(
                    ip=ip_address, device_type="nokia_sros_telnet", username="xxxx", password="xxx!", timeout=60)
                main_2(ip_address, node_name, connection)
                connection.disconnect()
        except:
            try:
                print(nodenum, "Connecting with ZTE SSH to", node_name)
                connection = netmiko.ConnectHandler(
                    ip=ip_address, device_type="zte_zxros", username="xxx", password="xxxx@xxx")
                print("Connected using SSH to", node_name)
                zte(ip_address, node_name, connection)
                connection.disconnect()
            except:
                print(nodenum, "Connecting with ZTE Telnet to", node_name)
                connection = netmiko.ConnectHandler(
                    ip=ip_address, device_type="zte_zxros_telnet", username="xxxx", password="xxxx@xxx")
                print("Connected using Telnet to", node_name)
                zte(ip_address, node_name, connection)
                connection.disconnect()
    except:
        print("Unable to connect")
        as_number.append("N/A")
        status.append('offline')
        node1_name.append(f'{node_name}')
        node_ip.append(f'{ip_address}')
        type_router.append("N/A")


with concurrent.futures.ThreadPoolExecutor(max_workers=250) as exector:
    for x in range(file.shape[0]):
        exector.submit(
            main, ip_address=file['Site ID'][x], node_name=file['Name'][x])
now_time = datetime.now().strftime("%d_%m_%y")
now_time_NF = datetime.now().strftime("%I_%M_%S %p")


# CREATING AND NAMING FILE
df_out = pd.DataFrame(list(zip(node_ip, node1_name, as_number, status, type_router)), columns=[
                      'IP Address', 'Router Name', 'AS Number', 'Status', "Router Type"])
df_out.to_excel(
    f'AS_Date_({now_time})__ Time_({now_time_NF}).xlsx', index=False)

# CREATING AND NAMING FILE
print(
    f"File AS_Date_({now_time})__ Time_({now_time_NF}).xlsx created \n Find it to see output")
print("End Time", datetime.now().strftime("%d/%m/%H:%M:%S"))
print("ROUTE Completed", "\n")

t2 = time.perf_counter()
print(f"Finished in {round(t2-t1,2)} Second(s)")
