import os
import pandas as pd
from datetime import datetime
IP_list = input("Drag and drop Shelf Document from NSP: ")
df = pd.read_csv(IP_list)
ping_stat = []
df_node = []
df_ip = []
print("Start Time", datetime.now().strftime("%d/%m/%H:%M:%S"))
for ip in range(df.shape[0]):
    ip_address = df['Site ID'][ip]
    node_name = df['Name'][ip]
    ping = os.popen(f'ping {ip_address} -n 2', mode='r').read()
    if "Approximate round trip" in ping:
        ping_stat.append('up')
        df_node.append(f'{node_name}')
        df_ip.append(f'{ip_address}')
    else:
        ping_stat.append('Offline')
        df_node.append(f'{node_name}')
        df_ip.append(f'{ip_address}')


now_time = datetime.now().strftime("%d/%m/%y-%H:%M:%S")
now_time_NF = datetime.now().strftime("%d%m%y-%H%M%S")
df_out = pd.DataFrame (list(zip(df_ip, df_node, ping_stat)), columns=['IP Address', 'Router Name', 'Ping Status'])
df_out.to_excel(f'Router_online_stat_{now_time_NF}.xlsx', index=False)
print(f"File Router_online_stat_{now_time_NF}.xlsx created \n Find it to see output")
print("End Time", datetime.now().strftime("%d/%m/%H:%M:%S"))
print("Test Completed")