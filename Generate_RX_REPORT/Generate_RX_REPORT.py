######
# oluwaseyimosobalaje.taiwo@gmail.com
######
# AUTOMATION Supports for PERFROM RX REPORT
######
import netmiko
from netmiko import ConnectHandler
from netmiko import NetmikoTimeoutException
from netmiko import NetmikoAuthenticationException
import pandas as pd
import re
import csv
from datetime import datetime
import pandas as pd
import concurrent.futures

print("Start Time", datetime.now().strftime("%d/%m/%y %I:%M:%S %p"))

NO_NAME = []
NO_IP = []
NO_PORT = []

NE_Name = []
Port_Name = []
Port_Description = []
Receive_Optical_Power_dBm = []
Lower_Threshold_Receive_Optical_Power = []
Transmit_Optical_Power_dBm = []
Lower_Threshold_Transmit_Optical_Power = []
SFP_value = []
Speed_value = []

nodenum = 0

ip_list = input("Drag and drop Document with IP's:")
file = pd.read_csv(ip_list)


def main_2(interfaces, NE_Name_1, Port_Name_1):
    global nodenum, NE_Name, Port_Name, Port_Description, Receive_Optical_Power_dBm, Lower_Threshold_Receive_Optical_Power, Transmit_Optical_Power_dBm, Lower_Threshold_Transmit_Optical_Power, SFP_value, Speed_value

    Description = re.compile(r"Description[ \t]{2,}: (?P<Description>.*)")
    speed = re.compile(r"Oper Speed[ \t]{2,}: (?P<speed>.*)")
    Temperature = re.compile(
        r"(?P<Name>Temperature \S+)[ \t]{2,}(?P<Value>[-\.\d+\!]+)[ \t]{2,}(?P<High_Alarm>[-\.\d+\!]+)[ \t]{2,}(?P<High_Warn>[-\.\d+\!]+)[ \t]{2,}(?P<Low_Warn>[-\.\d+\!]+)[ \t]{2,}(?P<Low_Alarm>[-\.\d+\!]+)")
    Supply_Voltage = re.compile(
        r"(?P<Name>Supply Voltage \S+)[ \t]{2,}(?P<Value>[-\.\d+\!]+)[ \t]{2,}(?P<High_Alarm>[-\.\d+\!]+)[ \t]{2,}(?P<High_Warn>[-\.\d+\!]+)[ \t]{2,}(?P<Low_Warn>[-\.\d+\!]+)[ \t]{2,}(?P<Low_Alarm>[-\.\d+\!]+)")
    Tx_Bias_Current = re.compile(
        r"(?P<Name>Tx Bias Current \S+)[ \t]{2,}(?P<Value>[-\.\d+\!]+)[ \t]{2,}(?P<High_Alarm>[-\.\d+\!]+)[ \t]{2,}(?P<High_Warn>[-\.\d+\!]+)[ \t]{2,}(?P<Low_Warn>[-\.\d+\!]+)[ \t]{2,}(?P<Low_Alarm>[-\.\d+\!]+)")
    Tx_Output_Power = re.compile(
        r"(?P<Name>Tx Output Power \S+)[ \t]{2,}(?P<Value>[-\.\d+\!]+)[ \t]{2,}(?P<High_Alarm>[-\.\d+\!]+)[ \t]{2,}(?P<High_Warn>[-\.\d+\!]+)[ \t]{2,}(?P<Low_Warn>[-\.\d+\!]+)[ \t]{2,}(?P<Low_Alarm>[-\.\d+\!]+)")
    Rx_Optical_Power = re.compile(
        r"(?P<Name>Rx Optical Power \S+ \S+)[ \t]{2,}(?P<Value>[-\.\d+\!]+)[ \t]{2,}(?P<High_Alarm>[-\.\d+\!]+)[ \t]{2,}(?P<High_Warn>[-\.\d+\!]+)[ \t]{2,}(?P<Low_Warn>[-\.\d+\!]+)[ \t]{2,}(?P<Low_Alarm>[-\.\d+\!]+)")
    Link_Length_support = re.compile(r"Link Length support: (?P<SFP>\S+).+")

    Description_match = Description.finditer(interfaces)
    speed_match = speed.finditer(interfaces)
    Temperature_match = Temperature.finditer(interfaces)
    Supply_Voltage_match = Supply_Voltage.finditer(interfaces)
    Tx_Bias_Current_match = Tx_Bias_Current.finditer(interfaces)
    Tx_Output_Power_match = Tx_Output_Power.finditer(interfaces)
    Rx_Optical_Power_match = Rx_Optical_Power.finditer(interfaces)
    Link_Length_support_match = Link_Length_support.finditer(interfaces)

    list_1 = []
    for x in Description_match:
        list_1.append(x.groupdict())
        for x in speed_match:
            list_1.append(x.groupdict())
            for x in Temperature_match:
                list_1.append(x.groupdict())
                for x in Supply_Voltage_match:
                    list_1.append(x.groupdict())
                    for x in Tx_Bias_Current_match:
                        list_1.append(x.groupdict())
                        for x in Tx_Output_Power_match:
                            list_1.append(x.groupdict())
                            for x in Rx_Optical_Power_match:
                                list_1.append(x.groupdict())
                                for x in Link_Length_support_match:
                                    list_1.append(x.groupdict())

    if float(list_1[6]["Value"].strip("!")) <= float(list_1[6]["Low_Warn"].strip("!")):
        NE_Name.append(f'{NE_Name_1}')
        Port_Name.append(f'{Port_Name_1}')
        Port_Description.append(f'{list_1[0]["Description"]}')
        Receive_Optical_Power_dBm.append(f'{list_1[6]["Value"]}')
        Lower_Threshold_Receive_Optical_Power.append(
            f'{list_1[6]["Low_Warn"]}')
        Transmit_Optical_Power_dBm.append(f'{list_1[5]["Value"]}')
        Lower_Threshold_Transmit_Optical_Power.append(
            f'{list_1[5]["Low_Warn"]}')
        SFP_value.append(f'{list_1[7]["SFP"]}')
        Speed_value.append(f'{list_1[1]["speed"]}')
        print("Done with ", NE_Name_1)
    else:
        print("Done with (+)", NE_Name_1)


def main(ip_address, NE_Name_1, Port_Name_1):
    global nodenum, NO_NAME, NO_IP, NO_PORT, NE_Name, Port_Name, Port_Description, Receive_Optical_Power_dBm, Lower_Threshold_Receive_Optical_Power, Transmit_Optical_Power_dBm, Lower_Threshold_Transmit_Optical_Power, SFP_value, Speed_value, nodenum
    nodenum += 1
    try:
        try:
            print('Node', nodenum, "...checking IP Address", ip_address, NE_Name_1)
            print("connecting with SSH")
            connection = netmiko.ConnectHandler(
                ip=ip_address, device_type="nokia_sros", username="xxxxxx", password="xxxxxx!")
            print("login to " + NE_Name_1 + " was successful")
            print('Connection successful, fetching the output...')
            port_num = (Port_Name_1.strip("-ddm")).lower()
            interfaces = (connection.send_command_timing(
                "show port " + port_num.strip("port")))
            main_2(interfaces, NE_Name_1, Port_Name_1)
        except:
            print("SSH not succesfull, trying telnet next")
            print("connecting with telnet")
            connection = netmiko.ConnectHandler(
                ip=ip_address, device_type="nokia_sros_telnet", username="xxxxxx", password="xxxxx!")
            print("login to " + NE_Name_1 + " was successful")
            print('Connection successful, fetching the output...')
            port_num = (Port_Name_1.strip("-ddm")).lower()
            interfaces = (connection.send_command_timing(
                "show port " + port_num.strip("port")))
            main_2(interfaces, NE_Name_1, Port_Name_1)
    except:
        print("could not check", NE_Name_1, "\n \n")
        NO_NAME.append(f'{NE_Name_1}')
        NO_IP.append(f'{ip_address}')
        NO_PORT.append(f'{(Port_Name_1.strip("-ddm")).lower()}')


with concurrent.futures.ThreadPoolExecutor(max_workers=120) as exector:
    for X in range(file.shape[0]):
        exector.submit(main, ip_address=file['Site ID'][X],
                       NE_Name_1=file['Site Name'][X], Port_Name_1=file['Object Name'][X])

now_time = datetime.now().strftime("%d_%m_%y")
now_time_NF = datetime.now().strftime("%I_%M_%S %p")
# CREATING AND NAMING FILE
df_out = pd.DataFrame(list(zip(NE_Name, Port_Name, Port_Description, Receive_Optical_Power_dBm, Lower_Threshold_Receive_Optical_Power, Transmit_Optical_Power_dBm, Lower_Threshold_Transmit_Optical_Power, SFP_value, Speed_value)), columns=[
                      'NE Name', 'Port Name', 'Port Description', 'Receive Optical Power(dBm)', 'Lower Threshold for Receive Optical Power(dBm)', 'Transmit Optical Power(dBm)', 'Lower Threshold for Transmit Optical Power(dBm)', 'SFP', 'Opr-Speed'])
df_NO = pd.DataFrame(list(zip(NO_NAME, NO_IP, NO_PORT)),
                     columns=['NE Name', 'IP', "Port"])
df_out.to_excel(
    f'RX_OUTPUT_Date_({now_time})__ Time_({now_time_NF}).xlsx', index=False)
df_NO.to_excel(
    f'RX_OUTPUT_Failed_Date_({now_time})__ Time_({now_time_NF}).xlsx', index=False)
# CREATING AND NAMING FILE
print(f"File RX_OUTPUT_Date_({now_time})__ Time_({now_time_NF}).xlsx created")
print(
    f"File RX_OUTPUT_Failed_Date_({now_time})__ Time_({now_time_NF}).xlsx created \nFind it to see output")
print("End Time", datetime.now().strftime("%d/%m/%H:%M:%S"))
print("RX Completed")
