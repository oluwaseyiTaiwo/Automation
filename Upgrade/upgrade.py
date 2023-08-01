import pandas as pd
import netmiko
from netmiko import ConnectHandler
from ntc_templates.parse import parse_output
from datetime import datetime
import concurrent.futures
import time
import re

t1= time.perf_counter()
print("Remote_Ping_Test_Start Time", datetime.now().strftime("%d/%m/%y %I:%M:%S %p"))

SITE_NAME =[]
SITE_IP=[]
Status_1 = []

ip_list=(input("Drag and drop Document with IP's:")).strip('"')
file=pd.read_csv(ip_list)
nodenum = 0

def nokia(ip_address,node_name,connection):
    global SITE_NAME,SITE_IP,Status_1,nodenum
    router_name = (connection.send_command("show system information",delay_factor=10))
    System_Name= re.compile(r"System Name[ \t]{2,}: (?P<System_Name>.*)")
    System_Name_match = System_Name.finditer(router_name)
    
    list_20=[]    
    for x in System_Name_match:
        list_20.append(x.groupdict())

    if "SAR8" in (list_20[0]["System_Name"]):
        card = (connection.send_command("show card"))
        Active_Standby=[x for x in card.split() if x.startswith(("A","B","Standby","Active"))]
        if "down" in card:
            SITE_NAME.append(node_name)
            SITE_IP.append(ip_address)
            Status_1.append("Card Issue")
        else:
            check_1234=connection.send_command("file version check cf3:\\TiMOS-B-20.10.R1\\boot.ldr")
            check_5678=connection.send_command("file version check cf3:\\TiMOS-B-20.10.R1\\both.tim")
            check_9123=connection.send_command("file version check cf3:\\TiMOS-B-20.10.R1\\support.tim")
            if ("OK" not in check_1234) and ("OK" not in check_5678) and ("OK" not in check_9123):
                SITE_NAME.append(node_name)
                SITE_IP.append(ip_address)
                Status_1.append("Image Issue")
            else:
                SOFT = (connection.send_command("show version",delay_factor=1))
                Software_version= re.compile(r"(?P<Software_version>TiMOS\S+)")
                Software_version_match = Software_version.finditer(SOFT)
                list_1=[]    
                for x in Software_version_match:
                    list_1.append(x.groupdict())
                Software=list_1[0]["Software_version"]

                connection.send_command ("file md " + "cf3-a:\\"+Software)
                connection.send_command ("file md " + "cf3-b:\\"+Software)

                pri = (connection.send_command("show bof",delay_factor=1))
                primary_config = re.compile(r"[ \t]{2,}primary-config[ \t]{2,}(?P<primary_config>.*)")
                primary_image=re.compile(r"[ \t]{2,}primary-image[ \t]{2,}(?P<primary_image>.*)")
                primary_config_match = primary_config.finditer(pri)  
                primary_image_match=primary_image.finditer(pri)

                for x in primary_config_match:
                    list_1.append(x.groupdict())
                for x in primary_image_match:
                    list_1.append(x.groupdict()) 
                
                primary=list_1[1]["primary_config"]
                secondary=list_1[2]["primary_image"]
                primary_1=primary.replace("cfg","ndx")

                primary_x=primary.strip("cf3:\\")
                primary_1_x=primary_1.strip("cf3:\\")

                d_1=connection.send_command_timing("file copy "+ primary + " cf3-a:\\"+ Software + "\\" + primary_x + "."+ Software)
                if "Overwrite" in d_1:
                    connection.send_command_timing("n")
                else:
                    pass
                
                d_2=connection.send_command_timing("file copy "+ primary_1 + " cf3-a:\\"+ Software + "\\" + primary_1_x + "."+ Software)
                if "Overwrite" in d_2:
                    connection.send_command_timing("n")
                else:
                    pass
                
                d_3=connection.send_command_timing("file copy "+ "cf3:\\"+"bof.cfg" + " cf3-a:\\"+ Software + "\\" + "bof.cfg" + "."+ Software)
                if "Overwrite" in d_2:
                    connection.send_command_timing("n")
                else:
                    pass
                
                d_4=connection.send_command_timing("file copy "+ primary + " cf3-b:\\"+ Software + "\\" + primary_x + "."+ Software)
                if "Overwrite" in d_1:
                    connection.send_command_timing("n")
                else:
                    pass
                
                d_5=connection.send_command_timing("file copy "+ primary_1 + " cf3-b:\\"+ Software + "\\" + primary_1_x + "."+ Software)
                if "Overwrite" in d_2:
                    connection.send_command_timing("n")
                else:
                    pass
                
                d_6=connection.send_command_timing("file copy "+ "cf3:\\"+"bof.cfg" + " cf3-b:\\"+ Software + "\\" + "bof.cfg" + "."+ Software)
                if "Overwrite" in d_2:
                    connection.send_command_timing("n")
                else:
                    pass

                d_7=connection.send_command_timing("file copy "+ "cf3:\\"+"boot.ldr" + " cf3-a:\\"+ Software + "\\" + "boot.ldr")
                if "Overwrite" in d_2:
                    connection.send_command_timing("n")
                else:
                    pass

                d_8=connection.send_command_timing("file copy "+ "cf3:\\"+"boot.ldr" + " cf3-b:\\"+ Software + "\\" + "boot.ldr")
                if "Overwrite" in d_2:
                    connection.send_command_timing("n")
                else:
                    pass

                
                if (Active_Standby[2]=="Active") and (Active_Standby[4]=="Standby"):
                    check_1=connection.send_command("file version check cf3:\\TiMOS-B-20.10.R1\\boot.ldr")
                    check_2=connection.send_command("file version check cf3:\\TiMOS-B-20.10.R1\\both.tim")
                    check_3=connection.send_command("file version check cf3:\\TiMOS-B-20.10.R1\\support.tim")
                    if ("OK" in check_1) and ("OK" in check_2) and ("OK" in check_3):
                        connection.send_command("file md cf3-b:\\TiMOS-B-20.10.R1")
                        a_1=connection.send_command_timing("file copy cf3:\\TiMOS-B-20.10.R1\\* cf3-b:\\TiMOS-B-20.10.R1")
                        if "Overwrite" in a_1:
                            connection.send_command_timing("n")
                            connection.send_command_timing("n")
                            connection.send_command_timing("n")
                        else:
                            pass
                        check_4=connection.send_command("file version check cf3-b:\\TiMOS-B-20.10.R1\\boot.ldr")
                        check_5=connection.send_command("file version check cf3-b:\\TiMOS-B-20.10.R1\\both.tim")
                        check_6=connection.send_command("file version check cf3-b:\\TiMOS-B-20.10.R1\\support.tim")
                    else:
                        print("Issue with router {} image".format(node_name))
                
                elif (Active_Standby[2]=="Standby") and (Active_Standby[4]=="Active"):
                    check_1=connection.send_command("file version check cf3:\\TiMOS-B-20.10.R1\\boot.ldr")
                    check_2=connection.send_command("file version check cf3:\\TiMOS-B-20.10.R1\\both.tim")
                    check_3=connection.send_command("file version check cf3:\\TiMOS-B-20.10.R1\\support.tim")
                    if ("OK" in check_1) and ("OK" in check_2) and ("OK" in check_3):
                        print("getting there")
                        connection.send_command("file md cf3-a:\\TiMOS-B-20.10.R1")
                        a_1=connection.send_command_timing("file copy cf3:\\TiMOS-B-20.10.R1\\* cf3-a:\\TiMOS-B-20.10.R1")
                        if "Overwrite" in a_1:
                            connection.send_command_timing("n")
                            connection.send_command_timing("n")
                            connection.send_command_timing("n")
                        else:
                            pass
                        check_4=connection.send_command("file version check cf3-a:\\TiMOS-B-20.10.R1\\boot.ldr")
                        check_5=connection.send_command("file version check cf3-a:\\TiMOS-B-20.10.R1\\both.tim")
                        check_6=connection.send_command("file version check cf3-a:\\TiMOS-B-20.10.R1\\support.tim")
                    else:
                        print("Issue with router {} image".format(node_name))

                dd_1=connection.send_command_timing("file copy cf3:\\TiMOS-B-20.10.R1\\boot.ldr cf3-a:\\boot.ldr")
                if "Overwrite" in dd_1:
                    connection.send_command_timing("y")
                else:
                    pass
                    
                dd_2=connection.send_command_timing("file copy cf3:\\TiMOS-B-20.10.R1\\boot.ldr cf3-b:\\boot.ldr")
                if "Overwrite" in dd_2:
                    connection.send_command_timing("y")
                else:
                    pass

                check_7=connection.send_command("file version check cf3-a:\\boot.ldr")   
                check_8=connection.send_command("file version check cf3-b:\\boot.ldr")
                if ("OK" in check_7) and ("OK" in check_8):
                    print("IMAGE OK")
                else:
                    print("Issue with router {} image".format(node_name))

                
                com_1=["bof","primary-image cf3:\\TiMOS-B-20.10.R1","secondary-image "+ secondary,"save","back","admin save"]
                connection.send_config_set(com_1)
                
                if (Active_Standby[2]=="Active") and (Active_Standby[4]=="Standby"):
                    gg_1=connection.send_command_timing("file copy cf3-a:\\bof.cfg cf3-b:\\bof.cfg")
                    if "Overwrite" in gg_1:
                        connection.send_command_timing("y")
                    else:
                        pass
                elif (Active_Standby[2]=="Standby") and (Active_Standby[4]=="Active"):
                    gg_1=connection.send_command("file copy cf3-b:\\bof.cfg cf3-a:\\bof.cfg")
                    if "Overwrite" in gg_1:
                        connection.send_command_timing("y")
                    else:
                        pass
                    
                SITE_NAME.append(node_name)
                SITE_IP.append(ip_address)
                Status_1.append("Done")

    elif "SASK12" in (list_20[0]["System_Name"]):
        check_123=connection.send_command("file version check cf1:\\TiMOS-B-20.9.R2\\boot.tim")
        if "OK" not in check_123:
            SITE_NAME.append(node_name)
            SITE_IP.append(ip_address)
            Status_1.append("Image Issue")
        else:
            SOFT = (connection.send_command("show version",delay_factor=1))
            Software_version= re.compile(r"(?P<Software_version>TiMOS\S+)")
            Software_version_match = Software_version.finditer(SOFT)
            list_1=[]    
            for x in Software_version_match:
                list_1.append(x.groupdict())
            Software=list_1[0]["Software_version"]

            connection.send_command("file md "+ Software)
            pri = (connection.send_command("show bof",delay_factor=1))
            primary_config = re.compile(r"[ \t]{2,}primary-config[ \t]{2,}(?P<primary_config>.*)")
            primary_image=re.compile(r"[ \t]{2,}primary-image[ \t]{2,}(?P<primary_image>.*)")
            primary_config_match = primary_config.finditer(pri)  
            primary_image_match=primary_image.finditer(pri)
            
            for x in primary_config_match:
                list_1.append(x.groupdict())
            for x in primary_image_match:
                list_1.append(x.groupdict()) 
            
            primary=list_1[1]["primary_config"]
            secondary=list_1[2]["primary_image"]
            primary_1=primary.replace("cfg","ndx")
            primary_2=primary.replace("cfg","sdx")
            primary_x=primary.strip("cf1:\\")
            primary_1_x=primary_1.strip("cf1:\\")
            primary_2_x=primary_2.strip("cf1:\\")

            d_1=connection.send_command_timing("file copy "+ primary + " cf1:\\"+ Software + "\\" + primary_x + "."+ Software)
            if "Overwrite" in d_1:
                connection.send_command_timing("n")
            else:
                pass
            d_2=connection.send_command_timing("file copy "+ primary_1 + " cf1:\\"+ Software + "\\" + primary_1_x + "."+ Software)
            if "Overwrite" in d_2:
                connection.send_command_timing("n")
            else:
                pass
            d_3=connection.send_command_timing("file copy "+ primary_2 + " cf1:\\"+ Software + "\\" + primary_2_x + "."+ Software)
            if "Overwrite" in d_3:
                connection.send_command_timing("n")
            else:
                pass
            d_4=connection.send_command_timing("file copy cf1:\\boot.tim cf1:\\"+ Software+"\\boot.tim")
            if "Overwrite" in d_4:
                connection.send_command_timing("n")
            else:
                pass
            check=connection.send_command("file version check cf1:\\TiMOS-B-20.9.R2\\boot.tim")
            if "OK" in check:
                connection.send_command_timing("file copy cf1:\\TiMOS-B-20.9.R2\\boot.tim cf1:\\boot.tim")
                connection.send_command_timing("y")
                print("images replaced")
            else:
                print("Issue with router {} image".format(node_name))
            
            check_2=connection.send_command("file version check cf1:\\boot.tim")

            if "OK" in check_2:
                print("image ok")
            else:
                print("Issue with router {} main image".format(node_name))

            com_1=["bof","primary-image cf1:\\TiMOS-B-20.9.R2","secondary-image "+ secondary,"save","back","admin save"]
            connection.send_config_set(com_1)

            SITE_NAME.append(node_name)
            SITE_IP.append(ip_address)
            Status_1.append("Done")

    elif "SASM" in (list_20[0]["System_Name"]):
        check_123=connection.send_command("file version check cf2:\\TiMOS-B-20.9.R2\\boot.tim")
        if "OK" not in check_123:
            SITE_NAME.append(node_name)
            SITE_IP.append(ip_address)
            Status_1.append("Image Issue")
        else:
            SOFT = (connection.send_command("show version",delay_factor=1))
            Software_version= re.compile(r"(?P<Software_version>TiMOS\S+)")
            Software_version_match = Software_version.finditer(SOFT)
            
            list_1=[]    
            for x in Software_version_match:
                list_1.append(x.groupdict())
            Software=list_1[0]["Software_version"]
        
            connection.send_command("file md "+ Software)
            pri = (connection.send_command("show bof",delay_factor=1))
            primary_config = re.compile(r"[ \t]{2,}primary-config[ \t]{2,}(?P<primary_config>.*)")
            primary_image=re.compile(r"[ \t]{2,}primary-image[ \t]{2,}(?P<primary_image>.*)")
            primary_config_match = primary_config.finditer(pri)  
            primary_image_match=primary_image.finditer(pri)
            
            for x in primary_config_match:
                list_1.append(x.groupdict())
            for x in primary_image_match:
                list_1.append(x.groupdict()) 
            
            primary=list_1[1]["primary_config"]
            secondary=list_1[2]["primary_image"]
            primary_1=primary.replace("cfg","ndx")
            primary_2=primary.replace("cfg","sdx")
            primary_x=primary.strip("cf2:\\")
            primary_1_x=primary_1.strip("cf2:\\")
            primary_2_x=primary_2.strip("cf2:\\")
            
            d_1=connection.send_command_timing("file copy "+ primary + " cf2:\\"+ Software + "\\" + primary_x + "."+ Software)
            if "Overwrite" in d_1:
                connection.send_command_timing("n")
            else:
                pass
            d_2=connection.send_command_timing("file copy "+ primary_1 + " cf2:\\"+ Software + "\\" + primary_1_x + "."+ Software)
            if "Overwrite" in d_2:
                connection.send_command_timing("n")
            else:
                pass
            d_3=connection.send_command_timing("file copy "+ primary_2 + " cf2:\\"+ Software + "\\" + primary_2_x + "."+ Software)
            if "Overwrite" in d_3:
                connection.send_command_timing("n")
            else:
                pass
            d_4=connection.send_command_timing("file copy cf2:\\boot.tim cf2:\\"+ Software+"\\boot.tim")
            if "Overwrite" in d_4:
                connection.send_command_timing("n")
            else:
                pass
        
            check=connection.send_command("file version check cf2:\\TiMOS-B-20.9.R2\\boot.tim")
            if "OK" in check:
                connection.send_command_timing("file copy cf2:\\TiMOS-B-20.9.R2\\boot.tim cf2:\\boot.tim")
                connection.send_command_timing("y")
                print("images replaced")
            else:
                print("Issue with router {} image".format(node_name))
            
            check_2=connection.send_command("file version check cf2:\\boot.tim")
            if "OK" in check_2:
                print("image ok")
            else:
                print("Issue with router {} main image".format(node_name))
            
            com_1=["bof","primary-image cf2:\\TiMOS-B-20.9.R2","secondary-image "+ secondary,"save","back","admin save"]
            connection.send_config_set(com_1)
            
            SITE_NAME.append(node_name)
            SITE_IP.append(ip_address)
            Status_1.append("Done")
    else:
        pass
    
def main(ip_address,node_name):
    global nodenum,SITE_NAME,SITE_IP,Status_1
    nodenum +=1
    try:
        try:
            print(nodenum,"Connecting with Nokia SSH to",node_name)
            connection=netmiko.ConnectHandler(ip=ip_address, device_type="nokia_sros", username="admin", password="Ng12345!")
            print("Connected using SSH to",node_name)
            nokia(ip_address,node_name,connection)
        except:
            print(nodenum,"Connecting with Nokia Telnet to",node_name)
            connection=netmiko.ConnectHandler(ip=ip_address, device_type="nokia_sros_telnet", username="admin", password="Ng12345!")
            print("Connected using Telnet to",node_name)
            nokia(ip_address,node_name,connection)
    except:
        SITE_NAME.append(node_name)
        SITE_IP.append(ip_address)
        Status_1.append("Offline")
with concurrent.futures.ThreadPoolExecutor(max_workers=100) as exector:
    for x in range(file.shape[0]):
        exector.submit(main,ip_address=file["Site ID"][x],node_name=file["Name"][x])

now_time = datetime.now().strftime("%d_%m_%y")
now_time_NF = datetime.now().strftime("%I_%M_%S %p")
## CREATING AND NAMING FILE
df_out_2=pd.DataFrame(list(zip(SITE_IP,SITE_NAME,Status_1)),columns=['IP Address', 'Router Name',"Status"])
df_out_2.to_excel(f'upgrade_Date_({now_time})__ Time_({now_time_NF}).xlsx', index=False)
## CREATING AND NAMING FILE
print(f"Result/upgrade_Date_({now_time})__ Time_({now_time_NF}).xlsx created \n Find it to see output")
print("End Time", datetime.now().strftime("%d/%m/%y %I:%M:%S %p"))
print("upgrade Completed")
t2= time.perf_counter()
print(f"Finished in {round(t2-t1,2)} Second(s)")