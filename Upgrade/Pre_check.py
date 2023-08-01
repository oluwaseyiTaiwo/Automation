import pandas as pd
import netmiko
from netmiko import ConnectHandler
import csv
from ntc_templates.parse import parse_output
from datetime import datetime
import time
import concurrent.futures
import re

ip_list = (input("Drag and drop Document with IP's:")).strip('"')
file = pd.read_csv(ip_list)

status = []
node1_name = []
node_ip = []
nodenum = 0


now_date1_NF = datetime.now().strftime("%d_%m_%y")
now_time1_NF = datetime.now().strftime("%I_%M_%S %p")
print("Start Time", datetime.now().strftime("%d/%m/%y %I:%M:%S %p"))


def main_2(ip_address, node_name, connection, display):
    global status, node1_name, node_ip, nodenum
    print('Connection successful, fetching the output...')
    print("login to " + node_name + " was successful")

    router_name = (connection.send_command(
        "show system information", delay_factor=10))
    System_Name = re.compile(r"System Name[ \t]{2,}: (?P<System_Name>.*)")
    System_Name_match = System_Name.finditer(router_name)
    list_20 = []
    for x in System_Name_match:
        list_20.append(x.groupdict())

    if "SAR8" in (list_20[0]["System_Name"]):
        with open(f'Command_SAR8.txt', "r") as Command:
            ROUTE_TABLE_config = Command.readlines()
            config_ROUTE_TABLE = connection.send_config_set(ROUTE_TABLE_config)
            print(config_ROUTE_TABLE, "\n", file=display)

    elif "SASK12" in (list_20[0]["System_Name"]):
        with open(f'Command_SASK12.txt', "r") as Command:
            ROUTE_TABLE_config = Command.readlines()
            config_ROUTE_TABLE = connection.send_config_set(ROUTE_TABLE_config)
            print(config_ROUTE_TABLE, "\n", file=display)

    elif "SASM" in (list_20[0]["System_Name"]):
        with open(f'Command_SASM.txt', "r") as Command:
            ROUTE_TABLE_config = Command.readlines()
            config_ROUTE_TABLE = connection.send_config_set(ROUTE_TABLE_config)
            print(config_ROUTE_TABLE, "\n", file=display)
    else:
        pass

    print("Done with ", node_name)
    status.append('Done')
    node1_name.append(f'{node_name}')
    node_ip.append(f'{ip_address}')


def main(ip_address, node_name):
    global status, node1_name, node_ip, nodenum
    nodenum += 1
    try:
        try:
            print('Node', nodenum, "...checking IP Address with SSH",
                  ip_address, node_name)
            print("connecting with SSH")
            connection = netmiko.ConnectHandler(
                ip=ip_address, device_type="nokia_sros", username="xxxx", password="xxxxx!xxxx", timeout=60)
            with open(f'Result/{node_name}_output_Date({now_date1_NF})__ Time({now_time1_NF}).txt', "a") as display:
                main_2(ip_address, node_name, connection, display)
                print("\n", "\n", file=display)
        except:
            print('Node', nodenum, "...checking IP Address with telnet",
                  ip_address, node_name)
            print("connecting with telnet")
            connection = netmiko.ConnectHandler(
                ip=ip_address, device_type="nokia_sros_telnet", username="xxxxx", password="xxxxxxxxxx", timeout=60)
            with open(f'Result/{node_name}_output_Date({now_date1_NF})__ Time({now_time1_NF}).txt', "a") as display:
                main_2(ip_address, node_name, connection, display)
                print("\n", "\n", file=display)
    except:
        status.append('Offline')
        node1_name.append(f'{node_name}')
        node_ip.append(f'{ip_address}')


with concurrent.futures.ThreadPoolExecutor(max_workers=5) as exector:
    for x in range(file.shape[0]):
        exector.submit(
            main, ip_address=file['Site ID'][x], node_name=file['Name'][x])

now_time = datetime.now().strftime("%d_%m_%y")
now_time_NF = datetime.now().strftime("%I_%M_%S %p")
# CREATING AND NAMING FILE
df_out = pd.DataFrame(list(zip(node_ip, node1_name, status)), columns=[
                      'IP Address', 'Router Name', 'Status'])
df_out.to_excel(
    f'Result/Pre_check_OUTPUT_Huawei_Date_({now_time})__ Time_({now_time_NF}).xlsx', index=False)
# CREATING AND NAMING FILE
print(
    f"Pre_check_OUTPUT_Huawei_Date_({now_time})__ Time_({now_time_NF}).xlsx created \n Find it to see output")
print("End Time", datetime.now().strftime("%d/%m/%H:%M:%S"))
print("Pre_check Completed", "\n")
