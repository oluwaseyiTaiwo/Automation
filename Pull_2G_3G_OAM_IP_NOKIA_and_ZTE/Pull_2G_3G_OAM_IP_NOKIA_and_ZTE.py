######
# oluwaseyimosobalaje.taiwo@gmail.com
######
# AUTOMATION Support for Pull_2G_3G_OAM_IP_ ON ENokia and ZTE routers
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

t1 = time.perf_counter()
print("Remote_Ping_Test_Start Time",
      datetime.now().strftime("%d/%m/%y %I:%M:%S %p"))

ip_list = (input("Drag and drop Document with IP's:")).strip('"')
file = pd.read_csv(ip_list)

now_date1_NF = datetime.now().strftime("%d_%m_%y")
now_time1_NF = datetime.now().strftime("%I_%M_%S %p")

router_name = []
ip_2G = []
ip = []
nodenum = 0
VPN_INSTANCE = []
router_type = []


def main_2(ip_address, node_name, connection):
    global router_name, ip_2G, ip, VPN_INSTANCE, router_type
    # CHANGE CHANGE COMMAND BASE ON THE TECH YOU WANT TO PULL (i.e 40201,40001,40701,40801)
    vprn = ["40001", "40701", "40801", "40201"]
    for y in vprn:
        arp = connection.send_command(
            "show router " + y + " arp", read_timeout=3)
        if "10." in arp:
            parsed_arp = [x for x in arp.split() if x.startswith(
                ("10.1", "10.2", "10.3", "10.4", "10.5", "10.6", "10.7", "10.8", "10.9", "10.0"))]
            for x in parsed_arp:
                router_name.append(node_name)
                ip_2G.append(x)
                ip.append(ip_address)
                if y == "40001":
                    VPN_INSTANCE.append("3G")
                elif y == "40201":
                    VPN_INSTANCE.append("OAM")
                elif y == "40801":
                    VPN_INSTANCE.append("2G")
                elif y == "40701":
                    VPN_INSTANCE.append("LTE")
                router_type.append("Nokia")
        else:
            router_name.append(node_name)
            ip_2G.append("NO IP")
            ip.append(ip_address)
            VPN_INSTANCE.append("N/A")
            router_type.append("Nokia")


def zte(ip_address, node_name, connection):
    global router_name, ip_2G, ip, VPN_INSTANCE, router_type
    vprn = ["40001", "40701", "40801", "40201"]
    for y in vprn:
        arp = connection.send_command("show arp vrf " + y, read_timeout=3)
        if "10." in arp:
            parsed_arp = [x for x in arp.split() if x.startswith(
                ("10.1", "10.2", "10.3", "10.4", "10.5", "10.6", "10.7", "10.8", "10.9", "10.0"))]
            for x in parsed_arp:
                router_name.append(node_name)
                ip_2G.append(x)
                ip.append(ip_address)
                if y == "40001":
                    VPN_INSTANCE.append("3G")
                elif y == "40201":
                    VPN_INSTANCE.append("OAM")
                elif y == "40801":
                    VPN_INSTANCE.append("2G")
                elif y == "40701":
                    VPN_INSTANCE.append("LTE")
                router_type.append("ZTE")
        else:
            router_name.append(node_name)
            ip_2G.append("NO IP")
            ip.append(ip_address)
            VPN_INSTANCE.append("N/A")
            router_type.append("ZTE")


def main(ip_address, node_name):
    global nodenum, router_name, ip_g, ip
    nodenum += 1
    try:
        try:
            try:
                print('Node', nodenum, "...checking IP Address with SSH",
                      ip_address, node_name)
                connection = netmiko.ConnectHandler(
                    ip=ip_address, device_type="nokia_sros", username="xx", password="xxx!", timeout=60)
                main_2(ip_address, node_name, connection)
                connection.disconnect()
            except:
                print('Node', nodenum, "...checking IP Address with TELNET",
                      ip_address, node_name)
                connection = netmiko.ConnectHandler(
                    ip=ip_address, device_type="nokia_sros_telnet", username="xxx", password="xxx!", timeout=60)
                main_2(ip_address, node_name, connection)
                connection.disconnect()
        except:
            try:
                print(nodenum, "Connecting with ZTE SSH to", node_name)
                connection = netmiko.ConnectHandler(
                    ip=ip_address, device_type="zte_zxros", username="xxxx", password="xxx@xxx")
                print("Connected using SSH to", node_name)
                zte(ip_address, node_name, connection)
                connection.disconnect()
            except:
                print(nodenum, "Connecting with ZTE Telnet to", node_name)
                connection = netmiko.ConnectHandler(
                    ip=ip_address, device_type="zte_zxros_telnet", username="xxxx", password="xx@xxx")
                print("Connected using Telnet to", node_name)
                zte(ip_address, node_name, connection)
                connection.disconnect()
    except:
        router_name.append(node_name)
        ip_2G.append("Router offline")
        ip.append(ip_address)
        VPN_INSTANCE.append("N/A")
        router_type.append("N/A")


with concurrent.futures.ThreadPoolExecutor(max_workers=2000) as exector:
    for x in range(file.shape[0]):
        exector.submit(
            main, ip_address=file["Site ID"][x], node_name=file["Name"][x])

now_time = datetime.now().strftime("%d_%m_%y")
now_time_NF = datetime.now().strftime("%I_%M_%S %p")

# CREATING AND NAMING FILE
df_out_1 = pd.DataFrame(list(zip(ip, router_name, ip_2G, VPN_INSTANCE, router_type)), columns=[
                        'Router IP Address', 'Router Name', "IP Address", "VPN_INSTANCE", "Router_Type"])
df_out_1.to_excel(
    f'Pull_2G_3G_OAM_IP_NOKIA_and_ZTE_({now_time})__ Time_({now_time_NF}).xlsx', index=False)

# CREATING AND NAMING FILE
print(
    f"Pull_2G_3G_OAM_IP_NOKIA_and_ZTE_({now_time})__ Time_({now_time_NF}).xlsx created \n Find it to see output")
print("End Time", datetime.now().strftime("%d/%m/%y %I:%M:%S %p"))
print("Pull_2G_3G_OAM_IP_NOKIA_and_ZTE Completed")
t2 = time.perf_counter()
print(f"Finished in {round(t2-t1,2)} Second(s)")
