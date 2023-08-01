######
# oluwaseyimosobalaje.taiwo@gmail.com
######
# Supports for AUTOMATION PULL_ISIS_NOKIA ON Nokia ROUTERS
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
print("Start Time",  datetime.now().strftime("%d/%m/%y %I:%M:%S %p"))
ip_list = input("Drag and drop Document with IP's:")

file = pd.read_csv(ip_list)
nodenum = 0

status = []
node1_name = []
node_ip = []

System_ID = []
State = []
Interface = []
node1_name_1 = []
node_ip_1 = []


def isis(ip_address, node_name, connection):
    global status, node1_name, node_ip, System_ID, State, Interface, node1_name_1, node_ip_1, nodenum
    isis_no = ["0", "1", "2", "6"]
    print('Connection successful, fetching the output...')
    print("login to " + node_name + " was successful")
    for Z in isis_no:
        interfaces = (connection.send_command(
            "show router isis " + Z + " adjacency"))
        print(interfaces)
        if ("not configured" in interfaces) or ("No Matching Entries" in interfaces):
            pass
        else:
            parsed_interface = parse_output(
                platform="alcatel_sros", command="show router isis adjacency", data=(interfaces))
            print(parsed_interface)
            for x in parsed_interface:
                System_ID.append(f'{x["system_id"]}')
                State.append(f'{x["state"]}')
                Interface.append(f'{x["interface"]}')
                node1_name_1.append(f'{node_name}')
                node_ip_1.append(f'{ip_address}')
    print("Done with", node_name, "\n")


def main(ip_address, node_name):
    global status, node1_name, node_ip, System_ID, State, Interface, node1_name_1, node_ip_1, nodenum
    nodenum += 1
    print('Node', nodenum, "...checking IP Address", ip_address, node_name)
    try:
        try:
            print("connecting with SSH")
            connection = netmiko.ConnectHandler(
                ip=ip_address, device_type="nokia_sros", username="xxxxxx", password="xxxx!")
            isis(ip_address, node_name, connection)
        except:
            print("connecting with TELNET")
            connection = netmiko.ConnectHandler(
                ip=ip_address, device_type="nokia_sros_telnet", username="xxxx", password="xxxxx!")
            isis(ip_address, node_name, connection)
    except:
        print("Unable to connect")
        status.append('Not Done')
        node1_name.append(f'{node_name}')
        node_ip.append(f'{ip_address}')


with concurrent.futures.ThreadPoolExecutor(max_workers=100) as exector:
    for x in range(file.shape[0]):
        exector.submit(
            main, ip_address=file['Site ID'][x], node_name=file['Name'][x])


now_time = datetime.now().strftime("%I_%M_%S %p")
now_time_NF = datetime.now().strftime("%d_%m_%y")
# CREATING AND NAMING FILE
df_out = pd.DataFrame(list(zip(node_ip, node1_name, status)), columns=[
                      'IP Address', 'Router Name', 'Status'])
df_out_1 = pd.DataFrame(list(zip(node_ip_1, node1_name_1, State, System_ID, Interface)), columns=[
                        'IP Address', 'Router Name', 'State', "System_ID", "Interface"])
df_out.to_excel(
    f'ISIS_OUTPUT_Failed_Date_({now_time})__ Time_({now_time_NF}).xlsx', index=False)
df_out_1.to_excel(
    f'ISIS_OUTPUT_Date_({now_time})__ Time_({now_time_NF}).xlsx', index=False)
# CREATING AND NAMING FILE
print(
    f"File ISIS_OUTPUT_Date_({now_time})__ Time_({now_time_NF}).xlsx created \n Find it to see output")
print(
    f"File ISIS_OUTPUT_Failed_Date_({now_time})__ Time_({now_time_NF}).xlsx created \n Find it to see output")
print("End Time",  datetime.now().strftime("%d/%m/%y %I:%M:%S %p"))
print("ISIS Check Completed")
