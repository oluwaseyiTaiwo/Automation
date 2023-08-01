######
# oluwaseyimosobalaje.taiwo@gmail.com
######
# AUTOMATION FOR PULLING  LINKS ON Nokia ROUTERS
######
######
import pandas as pd
import re
import netmiko
from netmiko import ConnectHandler
import csv
from ntc_templates.parse import parse_output
from datetime import datetime
import time
import concurrent.futures
print("Start Time",  datetime.now().strftime("%d/%m/%y %I:%M:%S %p"))
ip_list = (input("Drag and drop Document with IP's:")).strip('"')

file = pd.read_csv(ip_list)
nodenum = 0
Interface = []
Level = []
CircID = []
Oper_State = []
L1_L2_Metric = []
Router_name = []
Router_Ip = []
status = []
link_type = []


def isis(ip_address, node_name, connection):
    global status, Router_Ip, Router_name, L1_L2_Metric, Oper_State, CircID, Level, Interface, Router_name, Router_Ip, status
    isis_no = ["0", "1", "2", "6"]
    print('Connection successful, fetching the output...')
    print("login to " + node_name + " was successful")

    for Z in isis_no:
        interfaces = (connection.send_command_timing(
            "show router isis " + Z + " interface"))
        if ("not configured" in interfaces) or ("No Matching Entries" in interfaces):
            pass
        else:
            ISIS = re.compile(
                r"(?P<Interface>\S+)[ \t]{2,}(?P<Level>\S+)[ \t]{2,}(?P<CircID>[-\.\d+\!]+)[ \t]{2,}(?P<Oper_State>\S+)[ \t]{2,}(?P<Metric>\S+)")
            ISIS_match = ISIS.finditer(interfaces)

            list_1 = []
            for x in ISIS_match:
                list_1.append(x.groupdict())

            for x in range(len(list_1)):
                if list_1[x]["Interface"] != "system":
                    Interface.append(list_1[x]["Interface"])
                    Level.append(list_1[x]["Level"])
                    CircID.append(list_1[x]["CircID"])
                    Oper_State.append(list_1[x]["Oper_State"])
                    L1_L2_Metric.append((list_1[x]["Metric"]).strip("-"))
                    Router_name.append(node_name)
                    Router_Ip.append(ip_address)
                    status.append("Done")
                else:
                    pass


def main(ip_address, node_name):
    global nodenum, Router_Ip, Router_name, L1_L2_Metric, Oper_State, CircID, Level, Interface, Router_name, Router_Ip, status
    nodenum += 1
    print('Node', nodenum, "...checking IP Address", ip_address, node_name)
    try:
        try:
            print("connecting with SSH")
            connection = netmiko.ConnectHandler(
                ip=ip_address, device_type="nokia_sros", username="xxxxx", password="xxxxxxx!")
            isis(ip_address, node_name, connection)
            connection.disconnect()
        except:
            print("connecting with TELNET")
            connection = netmiko.ConnectHandler(
                ip=ip_address, device_type="nokia_sros_telnet", username="xxxxx", password="xxxx!")
            isis(ip_address, node_name, connection)
            connection.disconnect()
    except:
        print("Unable to connect")
        Interface.append("N/A")
        Level.append("N/A")
        CircID.append("N/A")
        Oper_State.append("N/A")
        L1_L2_Metric.append("N/A")
        Router_name.append(node_name)
        Router_Ip.append(ip_address)
        status.append("OFFLINE / NOT DONE")
        link_type.append("N/A")
        connection.disconnect()


with concurrent.futures.ThreadPoolExecutor(max_workers=300) as exector:
    for x in range(file.shape[0]):
        exector.submit(
            main, ip_address=file['Site ID'][x], node_name=file['Name'][x])


now_time = datetime.now().strftime("%I_%M_%S %p")
now_time_NF = datetime.now().strftime("%d_%m_%y")
# CREATING AND NAMING FILE
df_out_1 = pd.DataFrame(list(zip(Router_Ip, Router_name, Interface, Oper_State, L1_L2_Metric, CircID, Level, status)), columns=[
                        'IP Address', "Router Name", 'Interface Name', 'State', "Metric", "CircID", "Level", "status"])
df_out_1.to_excel(
    f'LINK_OUTPUT_Date_({now_time})__ Time_({now_time_NF}).xlsx', index=False)

# CREATING AND NAMING FILE
print(
    f"File LINK_OUTPUT_Date_({now_time})__ Time_({now_time_NF}).xlsx created \n Find it to see output")
print("End Time",  datetime.now().strftime("%d/%m/%y %I:%M:%S %p"))
print("LINK Check Completed")
