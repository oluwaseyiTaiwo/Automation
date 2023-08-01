######
#oluwaseyimosobalaje.taiwo@gmail.com
######
#AUTOMATION Support for Pushing Config to All nokia and ZTE routers
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

ip_list=(input("Drag and drop Document with IP's:")).strip('"')
file = pd.read_csv(ip_list)
file_2=""
status = []
node1_name = []
node_ip = []
nodenum = 0


now_date1_NF = datetime.now().strftime("%d_%m_%y")
now_time1_NF = datetime.now().strftime("%I_%M_%S %p")


with open(f'Result/ROUTE_Display_ Date({now_date1_NF})__ Time({now_time1_NF}).txt', "a") as display:
    print("Start Time", datetime.now().strftime("%d/%m/%y %I:%M:%S %p"))

    def main_2(ip_address,node_name,connection):
        global status,node1_name,node_ip,nodenum
        print('Connection successful, fetching the output...')
        print("login to " + node_name + " was successful")
        with open(f'Nokia_Command.txt', "r") as Command:
            ROUTE_TABLE_config=Command.readlines()
        config_ROUTE_TABLE=connection.send_config_set(ROUTE_TABLE_config)
        print(config_ROUTE_TABLE,"\n",file=display)
        status.append('Done')
        node1_name.append(f'{node_name}')
        node_ip.append(f'{ip_address}')
        print("Done with ",node_name)

    def zte(ip_address,node_name,connection):
        global status,node1_name,node_ip,nodenum
        print('Connection successful, fetching the output...')
        print("login to " + node_name + " was successful")
        with open(f'Zte_Command.txt', "r") as Command:
            ROUTE_TABLE_config=Command.readlines()
        config_ROUTE_TABLE=connection.send_config_set(ROUTE_TABLE_config)
        print(config_ROUTE_TABLE,"\n",file=display)
        status.append('Done')
        node1_name.append(f'{node_name}')
        node_ip.append(f'{ip_address}')
        print("Done with ",node_name)

    def main(ip_address,node_name):
        global status,node1_name,node_ip,nodenum
        nodenum +=1
        try:
            try:
                try:
                    print ('Node', nodenum, "...checking IP Address with SSH", ip_address, node_name)
                    print("connecting with SSH")
                    connection = netmiko.ConnectHandler(ip=ip_address, device_type= "nokia_sros",username= "admin", password= "Ng12345!",timeout=120)
                    main_2(ip_address,node_name,connection)
                    print("\n","\n",file=display)
                except:
                    print ('Node', nodenum, "...checking IP Address with TELNET", ip_address, node_name)
                    print("connecting with TELNET")
                    connection = netmiko.ConnectHandler(ip=ip_address, device_type= "nokia_sros_telnet", username= "admin", password= "Ng12345!",timeout=120)
                    main_2(ip_address,node_name,connection)
                    print("\n","\n",file=display)
            except:
                try:
                    print(nodenum,"Connecting with ZTE SSH to",node_name)
                    connection=netmiko.ConnectHandler(ip=ip_address, device_type="zte_zxros", username="Seyi", password="Seyi@321126")
                    print("Connected using SSH to",node_name)
                    zte(ip_address,node_name,connection)
                    print("\n","\n",file=display)
                except:
                    print(nodenum,"Connecting with ZTE Telnet to",node_name)
                    connection=netmiko.ConnectHandler(ip=ip_address, device_type="zte_zxros_telnet", username="Seyi", password="Seyi@321126")
                    print("Connected using Telnet to",node_name)
                    zte(ip_address,node_name,connection)
                    print("\n","\n",file=display)               
        except:
            print("Unable to connect")
            status.append('Not Done')
            node1_name.append(f'{node_name}')
            node_ip.append(f'{ip_address}')         
    with concurrent.futures.ThreadPoolExecutor(max_workers=50) as exector:
        for x in range(file.shape[0]):
            exector.submit(main,ip_address = file['Site ID'][x],node_name = file['Name'][x])
    now_time = datetime.now().strftime("%d_%m_%y")
    now_time_NF = datetime.now().strftime("%I_%M_%S %p")
    ## CREATING AND NAMING FILE
    df_out = pd.DataFrame (list(zip(node_ip, node1_name, status)), columns=['IP Address', 'Router Name', 'Status'])
    df_out.to_excel(f'Result/ROUTE_OUTPUT_Huawei_Date_({now_time})__ Time_({now_time_NF}).xlsx', index=False)
    ## CREATING AND NAMING FILE
    print(f"File ROUTE_OUTPUT_Huawei_Date_({now_time})__ Time_({now_time_NF}).xlsx created \n Find it to see output")
    print("End Time", datetime.now().strftime("%d/%m/%H:%M:%S"))
    print("ROUTE Completed","\n")