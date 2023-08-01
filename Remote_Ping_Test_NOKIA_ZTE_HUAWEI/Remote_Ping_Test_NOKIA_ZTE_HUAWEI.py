######
# oluwaseyimosobalaje.taiwo@gmail.com
######
# AUTOMATION Supports for REMOTE_REACHABILITY PING NOKIA HUAWEI AND ZTE
######
######

import pandas as pd
import netmiko
from netmiko import ConnectHandler
from ntc_templates.parse import parse_output
from datetime import datetime
import concurrent.futures
import time

t1 = time.perf_counter()
print("Remote_Ping_Test_NOKIA_ZTE_HUAWEI_Start Time",
      datetime.now().strftime("%d/%m/%y %I:%M:%S %p"))

Status = []
node_ip_list1 = []
node1_name_list1 = []
ip_list = (input("Drag and drop Document with IP's:")).strip('"')
file = pd.read_csv(ip_list)

nodenum = 0


def main(ip_address, node_name):
    global nodenum
    nodenum += 1
    try:
        try:
            try:
                try:
                    print(nodenum, "Connecting with SSH to", node_name)
                    connection = netmiko.ConnectHandler(
                        ip=ip_address, device_type="nokia_sros", username="xxx", password="xxxx!")
                    print("Connected using SSH to", node_name)
                    Status.append("Online")
                    node_ip_list1.append(ip_address)
                    node1_name_list1.append(node_name)
                except:
                    print(nodenum, "Connecting with Telnet to", node_name)
                    connection = netmiko.ConnectHandler(
                        ip=ip_address, device_type="nokia_sros_telnet", username="xxxx", password="xxxxxx!")
                    print("Connected using Telnet to", node_name)
                    Status.append("Online")
                    node_ip_list1.append(ip_address)
                    node1_name_list1.append(node_name)
            except:
                try:
                    print(nodenum, "Connecting with ZTE SSH to", node_name)
                    connection = netmiko.ConnectHandler(
                        ip=ip_address, device_type="zte_zxros", username="xxxxx", password="xxx@xxxxx")
                    print("Connected using SSH to", node_name)
                    Status.append("Online")
                    node_ip_list1.append(ip_address)
                    node1_name_list1.append(node_name)
                except:
                    print(nodenum, "Connecting with ZTE Telnet to", node_name)
                    connection = netmiko.ConnectHandler(ip=ip_address, device_type="zte_zxros_telnet", username="xxxxxx", password="xxxxx@"321126)
                    print("Connected using Telnet to", node_name)
                    Status.append("Online")
                    node_ip_list1.append(ip_address)
                    node1_name_list1.append(node_name)
        except:
            try:
                try:
                    print(nodenum, "Huawei Connecting using SSH to", node_name)
                    connection = netmiko.ConnectHandler(
                        ip=ip_address, device_type="huawei", username="xxxxx", password="xxx@xxxxx", global_delay_factor=0.1, timeout=10)
                    print(nodenum, "Huawei Connected using SSH to", node_name)
                    Status.append("Online")
                    node_ip_list1.append(ip_address)
                    node1_name_list1.append(node_name)
                except:
                    print(nodenum, "Datacom Connecting using SSH to", node_name)
                    connection = netmiko.ConnectHandler(
                        ip=ip_address, device_type="huawei", username="xxxx", password="xxxxxx@xxxx", global_delay_factor=0.1, timeout=10)
                    print(nodenum, "Datacom Connected using SSH to", node_name)
                    Status.append("Online")
                    node_ip_list1.append(ip_address)
                    node1_name_list1.append(node_name)
            except:
                try:
                    print(nodenum, "Huawei Connecting using SSH to", node_name)
                    connection = netmiko.ConnectHandler(
                        ip=ip_address, device_type="huawei_telnet", username="xxxxxx", password="xxxx@xxxx", global_delay_factor=0.1, timeout=10)
                    print(nodenum, "Huawei Connected using Telnet to", node_name)
                    Status.append("Online")
                    node_ip_list1.append(ip_address)
                    node1_name_list1.append(node_name)
                except:
                    print(nodenum, "Datacom Connecting using SSH to", node_name)
                    connection = netmiko.ConnectHandler(
                        ip=ip_address, device_type="huawei_telnet", username="xxxxxx", password="xxxxx@xxxx", global_delay_factor=0.1, timeout=10)
                    print(nodenum, "Datacom Connected using Telnet to", node_name)
                    Status.append("Online")
                    node_ip_list1.append(ip_address)
                    node1_name_list1.append(node_name)
    except:
        Status.append("Offline")
        node_ip_list1.append(ip_address)
        node1_name_list1.append(node_name)


with concurrent.futures.ThreadPoolExecutor(max_workers=1500) as exector:
    for x in range(file.shape[0]):
        exector.submit(
            main, ip_address=file["Site ID"][x], node_name=file["Name"][x])

now_time = datetime.now().strftime("%d_%m_%y")
now_time_NF = datetime.now().strftime("%I_%M_%S %p")
# CREATING AND NAMING FILE
df_out_1 = pd.DataFrame(list(zip(node_ip_list1, node1_name_list1, Status)), columns=[
                        'IP Address', 'Router Name', "Status"])
df_out_1.to_excel(
    f'Remote_Ping_Test_NOKIA_ZTE_HUAWEI_Date_({now_time})__ Time_({now_time_NF}).xlsx', index=False)
# CREATING AND NAMING FILE
print(
    f"Remote_Ping_Test_NOKIA_ZTE_HUAWEI_Date_({now_time})__ Time_({now_time_NF}).xlsx created \n Find it to see output")
print("End Time", datetime.now().strftime("%d/%m/%y %I:%M:%S %p"))
print("Remote Ping Test Completed")
t2 = time.perf_counter()
print(f"Finished in {round(t2-t1,2)} Second(s)")
