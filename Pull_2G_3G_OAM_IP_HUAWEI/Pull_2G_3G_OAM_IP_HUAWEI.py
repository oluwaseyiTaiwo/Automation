######
#oluwaseyimosobalaje.taiwo@gmail.com
######
#AUTOMATION Supports for Pulling _2G_3G_OAM_IP_HUAWEI
######
######

import pandas as pd
import netmiko
from netmiko import ConnectHandler
from ntc_templates.parse import parse_output
from datetime import datetime
import concurrent.futures
import time
import csv
import re

t1= time.perf_counter()
print("Remote_Ping_Test_Start Time", datetime.now().strftime("%d/%m/%y %I:%M:%S %p"))

ip_list=input("Drag and drop Document with IP's:")
file = pd.read_csv(ip_list)

now_date1_NF = datetime.now().strftime("%d_%m_%y")
now_time1_NF = datetime.now().strftime("%I_%M_%S %p")

IP_ADDRESS=[]
MAC_ADDRESS=[]
EXPIRE=[]
VLAN_TYPE=[]
INTERFACE=[]
VPN_INSTANCE=[]
Router_name=[]
Router_Ip=[]
status=[]
nodenum = 0


def main2(connection,node_name,ip_address):
    global status,Router_Ip,Router_name,VPN_INSTANCE,INTERFACE,VLAN_TYPE,EXPIRE,MAC_ADDRESS,IP_ADDRESS
    #CHANGE CHANGE COMMAND BASE ON THE TECH YOU WANT TO PULL (i.e ABIS,OAM,IUB,LTE)
    arp = connection.send_command("Dis arp all",read_timeout=10)
    arp_2=re.compile(r"(?P<IP_ADDRESS>\S+)[ \t]{2,}(?P<MAC_ADDRESS>\S+)[ \t]{2,}(?P<EXPIRE>\s+|\d+)[ \t]{2,}(?P<VLAN_TYPE>\S+ \S+|\S+)[ \t]{2,}(?P<INTERFACE>\S+)[ \t]{0,}(?P<VPN_INSTANCE>[\S+]*)")
    if "10." in arp:        
        arp_match = arp_2.finditer(arp)
        list_1=[]
        
        for x in arp_match:
            list_1.append(x.groupdict())
        
        for x in range(len(list_1)):
            if "Total" not in list_1[x]["IP_ADDRESS"]:
                IP_ADDRESS.append(list_1[x]["IP_ADDRESS"])
                MAC_ADDRESS.append(list_1[x]["MAC_ADDRESS"])
                EXPIRE.append(list_1[x]["EXPIRE"])
                VLAN_TYPE.append(list_1[x]["VLAN_TYPE"])
                INTERFACE.append(list_1[x]["INTERFACE"])
                VPN_INSTANCE.append(list_1[x]["VPN_INSTANCE"])
                Router_name.append(node_name)
                Router_Ip.append(ip_address)
                status.append("Done")
            else:
                pass
    else:
        IP_ADDRESS.append("N/A")
        MAC_ADDRESS.append("N/A")
        EXPIRE.append("N/A")
        VLAN_TYPE.append("N/A")
        INTERFACE.append("N/A")
        VPN_INSTANCE.append("N/A")
        Router_name.append(node_name)
        Router_Ip.append(ip_address)
        status.append("NO IP")

def main(ip_address,node_name):
    global nodenum,status,Router_Ip,Router_name,VPN_INSTANCE,INTERFACE,VLAN_TYPE,EXPIRE,MAC_ADDRESS,IP_ADDRESS
    nodenum +=1
    try:
        try:
            try:
                print(nodenum,"Huawei Connecting using SSH to",node_name) 
                connection = netmiko.ConnectHandler(ip=ip_address, device_type="huawei",username= "Datacom", password= "Ipran@123", global_delay_factor=0.1,timeout=10)
                print(nodenum,"Huawei Connected using SSH to",node_name)
                main2(connection,node_name,ip_address)
                connection.disconnect()
            except:
                print(nodenum,"Datacom Connecting using SSH to",node_name)
                connection = netmiko.ConnectHandler(ip=ip_address, device_type="huawei",username= "Huawei", password= "Admin@123", global_delay_factor=0.1,timeout=10)
                print(nodenum,"Datacom Connected using SSH to",node_name)
                main2(connection,node_name,ip_address)
                connection.disconnect()
        except:
            try:
                print(nodenum,"Huawei Connecting using SSH to",node_name)
                connection = netmiko.ConnectHandler(ip=ip_address, device_type="huawei_telnet",username="Datacom", password= "Ipran@123", global_delay_factor=0.1,timeout=10)
                print(nodenum,"Huawei Connected using Telnet to",node_name)
                main2(connection,node_name,ip_address) 
                connection.disconnect()
            except:
                print(nodenum,"Datacom Connecting using SSH to",node_name)
                connection = netmiko.ConnectHandler(ip=ip_address, device_type="huawei_telnet",username="Huawei", password= "Admin@123", global_delay_factor=0.1,timeout=10)
                print(nodenum,"Datacom Connected using Telnet to",node_name)
                main2(connection,node_name,ip_address)
                connection.disconnect()           
    except:
        IP_ADDRESS.append("N/A")
        MAC_ADDRESS.append("N/A")
        EXPIRE.append("N/A")
        VLAN_TYPE.append("N/A")
        INTERFACE.append("N/A")
        VPN_INSTANCE.append("N/A")
        Router_name.append(node_name)
        Router_Ip.append(ip_address)
        status.append("Offline")
        

with concurrent.futures.ThreadPoolExecutor(max_workers=1000) as exector:
    for x in range(file.shape[0]):
        exector.submit(main,ip_address=file["Site ID"][x],node_name=file["Name"][x])

now_time = datetime.now().strftime("%d_%m_%y")
now_time_NF = datetime.now().strftime("%I_%M_%S %p")


## CREATING AND NAMING FILE
df_out_1=pd.DataFrame(list(zip(Router_Ip,Router_name,IP_ADDRESS,INTERFACE,VLAN_TYPE,EXPIRE,MAC_ADDRESS,VPN_INSTANCE,status)),columns=['Router IP Address', 'Router Name',"IP Address","INTERFACE","VLAN_TYPE","EXPIRE","MAC_ADDRESS","VPN_INSTANCE","Status"])
df_out_1.to_excel(f'Pull_2G_3G_OAM_IP_HUAWEI_({now_time})__ Time_({now_time_NF}).xlsx', index=False)

## CREATING AND NAMING FILE
print(f"Pull_2G_3G_OAM_IP_HUAWEI_({now_time})__ Time_({now_time_NF}).xlsx created \n Find it to see output")
print("End Time", datetime.now().strftime("%d/%m/%y %I:%M:%S %p"))
print("Pull_2G_3G_OAM_IP_HUAWEI Completed")
t2= time.perf_counter()
print(f"Finished in {round(t2-t1,2)} Second(s)")