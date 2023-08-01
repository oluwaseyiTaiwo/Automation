######
#oluwaseyimosobalaje.taiwo@gmail.com
######
#AUTOMATION Support for PUSHING Config_Based_On_AS_NUMBER
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

ip_list=(input("Drag and drop Document with IP's:")).strip('"')
file = pd.read_csv(ip_list)

status = []
node1_name = []
node_ip = []
nodenum = 0


now_date1_NF = datetime.now().strftime("%d_%m_%y")
now_time1_NF = datetime.now().strftime("%I_%M_%S %p")


with open(f'ROUTE_Display_ Date({now_date1_NF})__ Time({now_time1_NF}).txt', "a") as display:
    print("Start Time", datetime.now().strftime("%d/%m/%y %I:%M:%S %p"))
    print("Start Time", datetime.now().strftime("%d/%m/%y %I:%M:%S %p"),"\n",file=display)

    def main_2(ip_address,node_name,connection):
        global status,node1_name,node_ip,nodenum
        print('Connection successful, fetching the output...')
        print("login to " + node_name + " was successful","\n",file=display)
        print("login to " + node_name + " was successful")
        
        As_number_output = (connection.send_command_timing("show router bgp neighbor"))
        As_number = re.compile(r"Local[ \t]{1,}AS[ \t]{2,}:[ \t]{1,}(?P<AS>\S+)")
        As_number_match =  As_number.finditer(As_number_output)


        list_1=[]
        for x in As_number_match:
            list_1.append(x.groupdict())  
                
        if list_1[0]["AS"] == "65131":
            with open(f'OYO_Region.txt', "r") as Command:
                ROUTE_TABLE_config=Command.readlines()
                config_ROUTE_TABLE=connection.send_config_set(ROUTE_TABLE_config)
                print(config_ROUTE_TABLE,"\n",file=display)
            status.append('Done')
            node1_name.append(f'{node_name}')
            node_ip.append(f'{ip_address}')
            print("Done with ",node_name)

        elif list_1[0]["AS"] == "65117":
            with open(f'Lagos_Region.txt', "r") as Command:
                ROUTE_TABLE_config=Command.readlines()
                config_ROUTE_TABLE=connection.send_config_set(ROUTE_TABLE_config)
                print(config_ROUTE_TABLE,"\n",file=display)
            status.append('Done')
            node1_name.append(f'{node_name}')
            node_ip.append(f'{ip_address}')
            print("Done with ",node_name)

        elif list_1[0]["AS"] == "65130":
            with open(f'EDO_Region_SAR8.txt', "r") as Command:
                ROUTE_TABLE_config=Command.readlines()
                config_ROUTE_TABLE=connection.send_config_set(ROUTE_TABLE_config)
                print(config_ROUTE_TABLE,"\n",file=display)
            status.append('Done')
            node1_name.append(f'{node_name}')
            node_ip.append(f'{ip_address}')
            print("Done with ",node_name)

        else:
            status.append('Uknown AS NUMBER')
            node1_name.append(f'{node_name}')
            node_ip.append(f'{ip_address}')
            print("Done with ",node_name)
        
        

    def main(ip_address,node_name):
        global status,node1_name,node_ip,nodenum
        nodenum +=1
        try:
            try:
                print ('Node', nodenum, "...checking IP Address with SSH", ip_address, node_name)
                print ('Node', nodenum, "...checking IP Address with SSH", ip_address, node_name,"\n",file=display)
                print("connecting with SSH")
                print("connecting with SSH","\n",file=display)
                connection = netmiko.ConnectHandler(ip=ip_address, device_type= "nokia_sros",username= "admin", password= "Ng12345!",timeout=60)
                main_2(ip_address,node_name,connection)
                print("\n","\n",file=display)
            except:
                print ('Node', nodenum, "...checking IP Address with TELNET", ip_address, node_name)
                print ('Node', nodenum, "...checking IP Address with TELNET", ip_address, node_name,"\n",file=display)
                print("connecting with TELNET")
                print("connecting with TELNET","\n",file=display)
                connection = netmiko.ConnectHandler(ip=ip_address, device_type= "nokia_sros_telnet", username= "admin", password= "Ng12345!",timeout=60)
                main_2(ip_address,node_name,connection)
                print("\n","\n",file=display)
        except:
            print("Unable to connect")
            print("Unable to connect","\n",file=display)
            status.append('Not Done')
            node1_name.append(f'{node_name}')
            node_ip.append(f'{ip_address}')  
            
    with concurrent.futures.ThreadPoolExecutor(max_workers=300) as exector:
        for x in range(file.shape[0]):
            exector.submit(main,ip_address = file['Site ID'][x],node_name = file['Name'][x])

    now_time = datetime.now().strftime("%d_%m_%y")
    now_time_NF = datetime.now().strftime("%I_%M_%S %p")
    ## CREATING AND NAMING FILE
    df_out = pd.DataFrame (list(zip(node_ip, node1_name, status)), columns=['IP Address', 'Router Name', 'Status'])
    df_out.to_excel(f'ROUTE_OUTPUT_Huawei_Date_({now_time})__ Time_({now_time_NF}).xlsx', index=False)
    ## CREATING AND NAMING FILE
    print(f"File ROUTE_OUTPUT_Huawei_Date_({now_time})__ Time_({now_time_NF}).xlsx created \n Find it to see output")
    print("End Time", datetime.now().strftime("%d/%m/%H:%M:%S"))
    print("End Time", datetime.now().strftime("%d/%m/%H:%M:%S"),"\n",file=display)
    print("ROUTE Completed","\n")
    print("ROUTE Completed","\n",file=display)