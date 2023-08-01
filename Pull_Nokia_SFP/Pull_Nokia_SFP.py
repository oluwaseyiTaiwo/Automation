######
#oluwaseyimosobalaje.taiwo@gmail.com
######
#AUTOMATION Support for pulling available nokia SFP 1. 100GBASE-LR \n 2. 10GBASE-LR \n 3. GIGE-LX \n 4. MDI GIGE-T \n 5. 10GBASE-ER"
######
######
import pandas as pd
import netmiko
from netmiko import ConnectHandler
from ntc_templates.parse import parse_output
from datetime import datetime
import concurrent.futures

t1= time.perf_counter()
print("Start Time", datetime.now().strftime("%d/%m/%y %I:%M:%S %p"))

c_qs_s_xfp_mdimdx_list = []
port_id_list = []
port_type_list = []
admin_state_list = []
port_state_list = []
node_ip_list = []
node1_name_list = []
Status = []
node_ip_list1 = []
node1_name_list1 = []

ip_list=(input("Drag and drop Document with IP's:")).strip('"')
file=pd.read_csv(ip_list)
nodenum = 0


print("Select SFP Type Your Searching For \n 1. 100GBASE-LR \n 2. 10GBASE-LR \n 3. GIGE-LX \n 4. MDI GIGE-T \n 5. 10GBASE-ER")
number=input("Enter SFP Type Your Searching For: ")
if number=="1":
    SFP_TYPE="100GBASE-LR"
elif number=="2":
    SFP_TYPE="10GBASE-LR"
elif number=="3":
    SFP_TYPE="GIGE-LX"
elif number=="4":
    SFP_TYPE="GIGE-T"
elif number=="5":
    SFP_TYPE="10GBASE-ER"

def main_2(ip_address,node_name,connection):
    global c_qs_s_xfp_mdimdx_list, port_id_list,port_type_list,admin_state_list,port_state_list,node_ip_list,node1_name_list,Status,node_ip_list1,node1_name_list1,nodenum
    print("login to " + node_name + " was successful")
    port = connection.send_command_timing("show port")
    parsed_port_output= parse_output(platform="alcatel_sros", command="show port", data=(port))
    for x in parsed_port_output:
        if (x['link']=='No') and (SFP_TYPE in x["c_qs_s_xfp_mdimdx"]):
            c_qs_s_xfp_mdimdx_list.append(x["c_qs_s_xfp_mdimdx"])
            port_id_list.append("Port "+ x["port_id"])
            port_type_list.append(x["port_type"])
            admin_state_list.append(x["admin_state"])
            port_state_list.append(x["port_state"])
            node_ip_list.append(ip_address)
            node1_name_list.append(node_name)
        else:
            pass
    print("Done with ",node_name)
   
def main(ip_address,node_name):
    global c_qs_s_xfp_mdimdx_list, port_id_list,port_type_list,admin_state_list,port_state_list,node_ip_list,node1_name_list,Status,node_ip_list1,node1_name_list1,nodenum
    nodenum +=1
    try:
        try:
            print(nodenum,"Connecting with SSH to",node_name)
            connection=netmiko.ConnectHandler(ip=ip_address, device_type="nokia_sros", username="admin", password="Ng12345!")
            print("Connected using SSH to",node_name)
            main_2(ip_address,node_name,connection)
            Status.append("DONE")
            node_ip_list1.append(ip_address)
            node1_name_list1.append(node_name)
            connection.disconnect()
        except:
            print(nodenum,"Connecting with Telnet to",node_name)
            connection=netmiko.ConnectHandler(ip=ip_address, device_type="nokia_sros_telnet", username="admin", password="Ng12345!")
            print("Connected using Telnet to",node_name)
            main_2(ip_address,node_name,connection)
            Status.append("DONE")
            node_ip_list1.append(ip_address)
            node1_name_list1.append(node_name)
            connection.disconnect()
    except:
        Status.append("Not DONE")
        node_ip_list1.append(ip_address)
        node1_name_list1.append(node_name)


with concurrent.futures.ThreadPoolExecutor(max_workers=1500) as exector:
    for x in range(file.shape[0]):
        exector.submit(main,ip_address=file["Site ID"][x],node_name=file["Name"][x])
now_time = datetime.now().strftime("%d_%m_%y")
now_time_NF = datetime.now().strftime("%I_%M_%S %p")

## CREATING AND NAMING FILE
df_out = pd.DataFrame (list(zip(node_ip_list, node1_name_list, admin_state_list,port_state_list, port_id_list,port_type_list,c_qs_s_xfp_mdimdx_list)), columns=['IP Address', 'Router Name', "Admin-State","Port_State","Port","Port-Type","SFP-Type"])
df_out_1=pd.DataFrame(list(zip(node_ip_list1,node1_name_list1,Status)),columns=['IP Address', 'Router Name',"Status"])
df_out.to_excel(f'SFP_OUTPUT_Date_({now_time})__ Time_({now_time_NF}).xlsx', index=False)
df_out_1.to_excel(f'SFP_OUTPUT_STATUS_Date_({now_time})__ Time_({now_time_NF}).xlsx', index=False)

## CREATING AND NAMING FILE
print(f"SFP_OUTPUT_Date_({now_time})__ Time_({now_time_NF}).xlsx created \n Find it to see output")
print(f"SFP_OUTPUT_STATUS_Date_({now_time})__ Time_({now_time_NF}).xlsx created \n Find it to see output")
print("End Time", datetime.now().strftime("%d/%m/%y %I:%M:%S %p"))
print("SFP Completed","\n")
t2= time.perf_counter()
print(f"Finished in {round(t2-t1,2)} Second(s)")
