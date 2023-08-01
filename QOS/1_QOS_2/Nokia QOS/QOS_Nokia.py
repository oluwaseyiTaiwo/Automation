######
# oluwaseyimosobalaje.taiwo@gmail.com
######
# Supports for AUTOMATION QOS TAGGING ON Nokia ROUTERS
######
######

import pandas as pd
import netmiko
from netmiko import ConnectHandler
import csv
from ntc_templates.parse import parse_output
from datetime import datetime
import time

ip_list = input("Drag and drop Document with IP's:")
file = pd.read_csv(ip_list)
status = []
node1_name = []
node_ip = []
nodenum = 1

now_date1_NF = datetime.now().strftime("%d_%m_%y")
now_time1_NF = datetime.now().strftime("%H_%M")
with open(f'QOS_Display_ Date({now_date1_NF})__ Time({now_time1_NF}).txt', "a") as display:
    print("Start Time", datetime.now().strftime("%d/%m/%H:%M:%S"))
    print("Start Time", datetime.now().strftime(
        "%d/%m/%H:%M:%S"), "\n", file=display)

    def interfaces_all(parsed_interface):
        count_0 = 0
        for z in range(0, len(parsed_interface)):
            if parsed_interface[z]["interface"] != "system" and parsed_interface[z]["interface"] != "loopback" and not parsed_interface[z]["interface"].startswith("CPAA") and not parsed_interface[z]["interface"].startswith("OAM") and not parsed_interface[z]["interface"].startswith("AF"):
                print(
                    "configuring " + parsed_interface[z]["interface"] + " interface", "\n", file=display)
                if "IXR" in node_name:
                    interface_configuration = ["/configure router interface " + parsed_interface[z]
                                               ["interface"], "info", "ingress qos 2000", "egress egress-remark-policy 1000"]

                else:
                    interface_configuration = [
                        "/configure router interface " + parsed_interface[z]["interface"], "info", "qos 2000"]

                config_interface = connection.send_config_set(
                    interface_configuration)
                print(config_interface, "\n", file=display)
                if ("invalid" in config_interface) or ("resources" in config_interface) or ("policy-id" in config_interface) or ("failed" in config_interface):
                    count_0 += 1
                else:
                    pass

            elif parsed_interface[z]["interface"] == "system":
                pass
        print("Done with interface", "\n", file=display)
        return count_0
        # print("\n \n")

    def vprn_interface_all():
        count_1 = 0
        vprn = ["40001", "40701", "40801"]
        for x in vprn:
            vprn_interface = (connection.send_command(
                "show router " + x + " interface"))
            if "Invalid router" in vprn_interface:
                print("No vprn interface on " + x)
            else:
                print(vprn_interface, "\n", file=display)
                check_1 = [F for F in vprn_interface.split()
                           if F.startswith("Entri")]
                if len(check_1) == 1:
                    print("doesnt have " + x + " service", "\n", file=display)
                else:
                    parsed_vprn_interface = parse_output(
                        platform="alcatel_sros", command="show router " + x + " interface", data=(vprn_interface))
                    print(parsed_vprn_interface, "\n", file=display)
                    # print("\n")

                    check_2 = ["/configure service vprn " + x, "info"]
                    print(connection.send_config_set(
                        check_2), "\n", file=display)
                    # print("\n")
                    for y in range(0, len(parsed_vprn_interface)):
                        if (parsed_vprn_interface[y]["port_sap_id"] != "n/a") and (parsed_vprn_interface[y]["port_sap_id"] != "loopback") and (parsed_vprn_interface[y]["port_sap_id"] != "rvpls") and (not parsed_vprn_interface[y]["port_sap_id"].startswith("spoke")):
                            if "SASM" in node_name:
                                vprn_configuration = ["/configure service vprn " + x, "interface " + parsed_vprn_interface[y]
                                                      ["interface"], "info", "sap " + parsed_vprn_interface[y]["port_sap_id"], "ingress qos 1000"]

                            elif "IXR" in node_name:
                                vprn_configuration = ["/configure service vprn " + x, "interface " + parsed_vprn_interface[y]["interface"],
                                                      "info", "sap " + parsed_vprn_interface[y]["port_sap_id"], "ingress qos 1000", "egress egress-remark-policy 1000"]

                            else:
                                vprn_configuration = ["/configure service vprn " + x, "interface " + parsed_vprn_interface[y]["interface"],
                                                      "info", "sap " + parsed_vprn_interface[y]["port_sap_id"], "ingress qos 1000", "egress qos 1000"]

                            config_vprn = connection.send_config_set(
                                vprn_configuration)
                            print(config_vprn, "\n", file=display)
                            if ("invalid" in config_vprn) or ("resources" in config_vprn) or ("policy-id" in config_vprn) or ("failed" in config_vprn):
                                count_1 += 1
                            else:
                                pass

                            # print("\n")
                        else:
                            pass
                print("Done with " + x, "\n", file=display)
        print("Done with vprn", "\n", file=display)
        return count_1
        # print("\n \n")

    def port_interface_all(parsed_interface):
        count_2 = 0
    # normal port config
        normalport = []
        for z in range(0, len(parsed_interface)):
            if parsed_interface[z]["port_sap_id"] != "system" and parsed_interface[z]["port_sap_id"] != "n/a" and parsed_interface[z]["port_sap_id"] != "rvpls" and parsed_interface[z]["port_sap_id"] != "loopback" and not parsed_interface[z]["port_sap_id"].startswith("lag"):
                normalport.append(parsed_interface[z]["port_sap_id"])
            else:
                pass

    # to remove :vlan
        normalport = [x.split(":", 1)[0] for x in normalport]
        print(normalport, "\n", file=display)
    # to remove :vlan

    # normal port config
        for x in range(0, len(normalport)):
            # CHECK PORT MODE
            check_1 = (connection.send_command("show port " + normalport[x]))
            check_2 = [y for y in check_1.split() if y.startswith(
                ("network", "access", "hybrid"))]
            print(check_2, "\n", file=display)
            # CHECK PORT MODE
            if check_2[0] == "network" or check_2[0] == "hybrid":
                print(
                    "port " + normalport[x] + " to be configured as network", "\n", file=display)
                if "SASM" in node_name:
                    normal_port_configuration = [
                        "/configure port " + normalport[x], "info", "ethernet", "network", " qos 2001"]
                    config_normal_port = connection.send_config_set(
                        normal_port_configuration)
                    print(config_normal_port, "\n", file=display)
                    if ("invalid" in config_normal_port) or ("resources" in config_normal_port) or ("policy-id" in config_normal_port) or ("failed" in config_normal_port):
                        count_2 += 1
                    else:
                        pass

                    # print("\n")
                elif "SASK" in node_name:
                    normal_port_configuration = [
                        "/configure port " + normalport[x], "info", "ethernet", "network", " qos 2000"]
                    config_normal_port = connection.send_config_set(
                        normal_port_configuration)
                    print(config_normal_port, "\n", file=display)
                    if ("invalid" in config_normal_port) or ("resources" in config_normal_port) or ("policy-id" in config_normal_port) or ("failed" in config_normal_port):
                        count_2 += 1
                    else:
                        pass
                else:
                    pass
                    # print("\n")
            elif check_2[0] == "access":
                if "SASM" in node_name:
                    normal_port_configuration = [
                        "/configure port " + normalport[x], "info", "ethernet", "access", "egress qos 1000"]
                    config_normal_port = connection.send_config_set(
                        normal_port_configuration)
                    print(config_normal_port, "\n", file=display)
                    if ("invalid" in config_normal_port) or ("resources" in config_normal_port) or ("policy-id" in config_normal_port) or ("failed" in config_normal_port):
                        count_2 += 1
                    else:
                        pass
                    # print("\n")
                else:
                    pass
            else:
                pass
        print("Done with normal port", "\n", file=display)
        # print("\n \n")

    # lag port config
        lagport_all = (connection.send_command("show lag port"))
        print(lagport_all, "\n", file=display)
        lagport = [x for x in lagport_all.split() if x.startswith(
            ("1/", "2/", "3/", "4/", "5/"))]
        print(lagport, "\n", file=display)
        # print("\n")
        for x in range(0, len(lagport)):
            # CHECK PORT MODE
            check_3 = (connection.send_command("show port " + lagport[x]))
            check_4 = [y for y in check_3.split() if y.startswith(
                ("network", "access", "hybrid"))]
            print(check_4, "\n", file=display)
            # CHECK PORT MODE

            if check_4[0] == "network" or check_4[0] == "hybrid":
                print(
                    "port " + lagport[x] + " to be configured as network", "\n", file=display)
                if "SASM" in node_name:
                    lag_port_configuration = [
                        "/configure port " + lagport[x], "info", "ethernet", "network", " qos 2001"]
                    config_lag_port = connection.send_config_set(
                        lag_port_configuration)
                    print(config_lag_port, "\n", file=display)
                    if ("invalid" in config_lag_port) or ("resources" in config_lag_port) or ("policy-id" in config_lag_port) or ("failed" in config_lag_port):
                        count_2 += 1
                    else:
                        pass
                    # print("\n")
                elif "SASK" in node_name:
                    lag_port_configuration = [
                        "/configure port " + lagport[x], "info", "ethernet", "network", " qos 2000"]
                    config_lag_port = connection.send_config_set(
                        lag_port_configuration)
                    print(config_lag_port, "\n", file=display)
                    if ("invalid" in config_lag_port) or ("resources" in config_lag_port) or ("policy-id" in config_lag_port) or ("failed" in config_lag_port):
                        count_2 += 1
                    else:
                        pass
                else:
                    pass
                    # print("\n")
            elif check_4[0] == "access":
                print(
                    "port " + lagport[x] + " to be configured as access", "\n", file=display)
                if "SASM" in node_name:
                    lag_port_configuration = [
                        "/configure port " + lagport[x], "info", "ethernet", "network", " qos 2001"]
                    config_lag_port = connection.send_config_set(
                        lag_port_configuration)
                    print(config_lag_port, "\n", file=display)
                    if ("invalid" in config_lag_port) or ("resources" in config_lag_port) or ("policy-id" in config_lag_port) or ("failed" in config_lag_port):
                        count_2 += 1
                    else:
                        pass
                else:
                    pass
            else:
                pass
                # print("\n")
        print("Done with lag port", "\n", file=display)
    # lag port config
        # print("\n")
        print("Done with port", "\n", file=display)
        # print("\n")
        return count_2

    def main():
        print('Connection successful, fetching the output...')
        print("login to " + node_name + " was successful", "\n", file=display)
        print("login to " + node_name + " was successful")
        interfaces = (connection.send_command("show router interface"))
        print(interfaces, "\n", file=display)
        parsed_interface = parse_output(
            platform="alcatel_sros", command="show router interface", data=(interfaces))
        # print("\n","\n")
        if "SASK" in node_name:
            x = 0
        else:
            x = interfaces_all(parsed_interface)
        y = port_interface_all(parsed_interface)
        z = vprn_interface_all()
        if (x > 0) or (y > 0) or (z > 0):
            status.append('Policy or resource issue')
            node1_name.append(f'{node_name}')
            node_ip.append(f'{ip_address}')
        else:
            status.append('Done')
            node1_name.append(f'{node_name}')
            node_ip.append(f'{ip_address}')

    for x in range(file.shape[0]):
        ip_address = file['Site ID'][x]
        node_name = file['Name'][x]
        print('Node', nodenum, "...checking IP Address", ip_address, node_name)
        print('Node', nodenum, "...checking IP Address",
              ip_address, node_name, "\n", file=display)
        nodenum += 1
        # time.sleep(4)
        try:
            try:
                print("connecting with SSH", "\n", file=display)
                connection = netmiko.ConnectHandler(
                    ip=ip_address, device_type="nokia_sros", username="xxxxxxxxx", password="xxxxxx!")
                # if "NIXR-E" in node_name:
                # print("ignore NIXR-E",node_name,"\n",file=display)
                # print("\n")
                # status.append('cant configure NIXR-E')
                # node1_name.append(f'{node_name}')
                # node_ip.append(f'{ip_address}')
                # else:
                main()
                print("\n", "\n", file=display)
            except:
                print("connecting with TELNET", "\n", file=display)
                connection = netmiko.ConnectHandler(
                    ip=ip_address, device_type="nokia_sros_telnet", username="xxxx", password="xxx!")
                # if "NIXR-E" in node_name:
                #  print("ignore NIXR-E",node_name,"\n",file=display)
                # print("\n")
                # status.append('cant configure NIXR-E')
                # node1_name.append(f'{node_name}')
                # node_ip.append(f'{ip_address}')
                # else:
                main()
                print("\n", "\n", file=display)

        except:
            print("Unable to connect", "\n", file=display)
            # print("\n")
            status.append('Not Done')
            node1_name.append(f'{node_name}')
            node_ip.append(f'{ip_address}')

    now_time = datetime.now().strftime("%d/%m/%y-%H:%M:%S")
    now_time_NF = datetime.now().strftime("%d_%m_%y-%H%M%S")
    # CREATING AND NAMING FILE
    df_out = pd.DataFrame(list(zip(node_ip, node1_name, status)), columns=[
                          'IP Address', 'Router Name', 'Status'])
    df_out.to_excel(f'QOS_OUTPUT_{now_time_NF}.xlsx', index=False)
    # CREATING AND NAMING FILE
    print(
        f"File QOS_OUTPUT_{now_time_NF}.xlsx created \n Find it to see output")
    print("End Time", datetime.now().strftime("%d/%m/%H:%M:%S"))
    print("End Time", datetime.now().strftime(
        "%d/%m/%H:%M:%S"), "\n", file=display)
    print("QOS Completed", "\n")
    print("QOS Completed", "\n", file=display)
