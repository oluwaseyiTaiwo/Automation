######
# oluwaseyimosobalaje.taiwo@gmail.com
######
# Supports for AUTOMATION QOS TAGGING ON HUAWEI ROUTERS
######
######
import pandas as pd
import netmiko
from netmiko import ConnectHandler
import csv
from ntc_templates.parse import parse_output
from datetime import datetime
import time

status = []
node1_name = []
node_ip = []
nodenum = 0
count_error = 0
count_done = 0
count_trunk_error = 0
count_error_list = []
count_done_list = []
count_trunk_error_list = []
node_ip_error = []
port_error = []
node1_name_error = []
status_1 = []


ip_list = input("Drag and drop Document with IP's:")
file = pd.read_csv(ip_list)
now_date1_NF = datetime.now().strftime("%d_%m_%y")
now_time1_NF = datetime.now().strftime("%H_%M")


def main():
    interfaces = connection.send_command("display interface brief")
    # print(interfaces)
    parsed_interface = parse_output(
        platform="huawei_vrp", command="display interface brief", data=(interfaces))
    # print(parsed_interface)
    count_error = 0
    count_done = 0
    count_trunk_error = 0
    print("Working")
    for x in parsed_interface:
        if x['phy'] != "*down" and x['interface'].startswith(("GigabitEthernet", "Eth-Trunk")):
            interface_name = x['interface'].split("(")[0]
            # print(interface_name)
            print(interface_name, "\n", file=display)
            qos_config = ["int " + interface_name,
                          "trust upstream default", "trust 8021p", "commit", "return"]
            config_qos = connection.send_config_set(
                qos_config, delay_factor=0.1)
            print(config_qos, "\n", file=display)

            if "Please remove the interface from the trunk first" in config_qos:
                count_trunk_error += 1
                node_ip_error.append(f'{ip_address}')
                port_error.append(f'{interface_name}')
                node1_name_error.append(f'{node_name}')
                status_1.append('Trunk-Error')
            elif "Error" in config_qos:
                count_error += 1
                node_ip_error.append(f'{ip_address}')
                port_error.append(f'{interface_name}')
                node1_name_error.append(f'{node_name}')
                status_1.append('Other-Error')
            else:
                count_done += 1
        else:
            pass

    save = connection.save_config("save")
    print(save, "\n", file=display)
    print("Done with", node_name)
    print("Done with", node_name, "\n", file=display)
    connection.disconnect()

    status.append('Done')
    node1_name.append(f'{node_name}')
    node_ip.append(f'{ip_address}')
    count_error_list.append(f'{count_error}')
    count_done_list.append(f'{count_done}')
    count_trunk_error_list.append(f'{count_trunk_error}')


with open(f'QOS_Huawei_Display_ Date({now_date1_NF})__ Time({now_time1_NF}).txt', "a") as display:
    print("Start Time", datetime.now().strftime("%d/%m/%H:%M:%S"))
    print("Start Time", datetime.now().strftime(
        "%d/%m/%H:%M:%S"), "\n", file=display)
    for x in range(file.shape[0]):
        ip_address = file['Site ID'][x]
        node_name = file['Name'][x]
        nodenum += 1
        try:
            try:
                try:
                    print(nodenum, "Huawei Connecting with SSH to", node_name)
                    print(nodenum, "Huawei Connecting with SSH to",
                          node_name, "\n", file=display)

                    connection = netmiko.ConnectHandler(
                        ip=ip_address, device_type="huawei", username="xxxxxx", password="xxxxxxxxxxxx", global_delay_factor=0.1, timeout=10)

                    print("Huawei Connected using SSH to", node_name)
                    print("Huawei Connected using SSH to",
                          node_name, "\n", file=display)
                    main()
                except:
                    print(nodenum, "Datacom Connecting with SSH to", node_name)
                    print(nodenum, "Datacom Connecting with SSH to",
                          node_name, "\n", file=display)
                    connection = netmiko.ConnectHandler(
                        ip=ip_address, device_type="huawei", username="xxx", password="xxxxxxxx", global_delay_factor=0.1)
                    print("Datacom Connected using SSH to", node_name)
                    print("Datacom Connected using SSH to",
                          node_name, "\n", file=display)
                    main()
            except:
                try:
                    print(nodenum, "Huawei Connecting with TELNET to", node_name)
                    print(nodenum, "Huawei Connecting with TELNET to",
                          node_name, "\n", file=display)
                    connection = netmiko.ConnectHandler(
                        ip=ip_address, device_type="huawei_telnet", username="xxx", password="xxxxxx", global_delay_factor=0.1, timeout=10)
                    print("Huawei Connected using Telnet to", node_name)
                    print("Huawei Connected using Telnet to",
                          node_name, "\n", file=display)
                    main()
                except:
                    print(nodenum, "Datacom Connecting with TELNET to", node_name)
                    print(nodenum, "Datacom Connecting with TELNET to",
                          node_name, "\n", file=display)
                    connection = netmiko.ConnectHandler(
                        ip=ip_address, device_type="huawei_telnet", username="xxxxx", password="xxxxx", global_delay_factor=0.1)
                    print("Datacom Connected using Telnet to", node_name)
                    print("Datacom Connected using Telnet to",
                          node_name, "\n", file=display)
                    main()
        except:
            print("Unable to connect")
            print("Unable to connect", "\n", file=display)
            status.append('Not Done')
            node1_name.append(f'{node_name}')
            node_ip.append(f'{ip_address}')
            count_error_list.append(f'{count_error}')
            count_done_list.append(f'{count_done}')
            count_trunk_error_list.append(f'{count_trunk_error}')

    now_time = datetime.now().strftime("%d/%m/%y-%H:%M:%S")
    now_time_NF = datetime.now().strftime("%d_%m_%y-%H%M%S")
    # CREATING AND NAMING FILE
    df_out = pd.DataFrame(list(zip(node_ip, node1_name, status, count_done_list, count_error_list, count_trunk_error_list)), columns=[
                          'IP Address', 'Router Name', 'Status', "Done", "Other-Error", "Trunk-Error"])
    df_out.to_excel(f'QOS_OUTPUT_Huawei_{now_time_NF}.xlsx', index=False)

    df_out_1 = pd.DataFrame(list(zip(node_ip_error, node1_name_error, port_error, status_1)), columns=[
                            'IP Address', 'Router Name', "Interface-Port", "Error"])
    df_out_1.to_excel(
        f'QOS_OUTPUT_Huawei_Port_ERROR{now_time_NF}.xlsx', index=False)

    # CREATING AND NAMING FILE
    print(
        f"File QOS_OUTPUT_Huawei_{now_time_NF}.xlsx created \n Find it to see output")
    print(
        f"File QOS_OUTPUT_Huawei_{now_time_NF}.xlsx created \n Find it to see output", "\n", file=display)
    print(
        f"File QOS_OUTPUT_Huawei_Port_ERROR{now_time_NF}.xlsx created \n Find it to see output")
    print(
        f"File QOS_OUTPUT_Huawei_Port_ERROR{now_time_NF}.xlsx created \n Find it to see output", "\n", file=display)
    print("End Time", datetime.now().strftime("%d/%m/%H:%M:%S"))
    print("End Time", datetime.now().strftime(
        "%d/%m/%H:%M:%S"), "\n", file=display)
    print("QOS Completed", "\n")
    print("QOS Completed", "\n", file=display)
