######
#tundeakingbade11@gmail.com and oluwaseyimosobalaje.taiwo@gmail.com
######
#Supports Moba-Xterm 20.5 but the script can be modified to support any terminal program that can export its nodes as an editable file.
######
######
import pandas as pd
from datetime import datetime


#Creating csv file using time and date in other not to overwrite existing file
now = datetime.now()
f = now.strftime("Result/MobaXterm Sesions-%d-%m-%H%M.mxtsessions")
new_file = open(f, "w", newline="")

########################################
# Open file containing IP addresses
########################################

# Open file containing Nokia IP addresses
nokia_NE_list = (input("Nokia list to work with: ")).strip('"')
df_NK = pd.read_csv(nokia_NE_list)

zte_NE_list = (input("Zte list to work with: ")).strip('"')
df_zte = pd.read_csv(zte_NE_list)

# Open file containing Huawei IP addresses
huawei_NE_list = (input("Huawei list to work with: ")).strip('"')
df_HW = pd.read_csv(huawei_NE_list, skiprows=3)


new_file.write('[Bookmarks]\n')
new_file.write('SubRep=\n')
new_file.write('ImgNum=42\n')


###############################
# For Huawei List
###############################

new_file.write('ImgNum=41\n')

new_file.write('[Bookmarks_1]\n')
new_file.write('SubRep=Huawei\n')
new_file.write('ImgNum=41\n')

for d in range(0, df_HW.shape[0]):
    node = df_HW['NE Name'][d]
    IP = df_HW['NE IP Address'][d]
    
    new_file.write(f'{node}= #129#1%{IP}%23%%%2%%%%%0%0%%1080%#MobaFont%10%0%0%-1%15%236,236,236%30,30,30%180,180,192%0%-1%0%%xterm%-1%-1%_Std_Colors_0_%80%24%0%1%-1%<none>%%0#0# #-1\n')

###############################
# For Nokia List
###############################
new_file.write('\n')
new_file.write('[Bookmarks_2]\n')
new_file.write('SubRep=Nokia\n')
new_file.write('ImgNum=41\n')

for d in range(0, df_NK.shape[0]):
    node = df_NK['Name'][d]
    IP = df_NK['Site ID'][d]
    if "SASK" in node: #SSH is the prefered method of login
        new_file.write(f'{node} =  #130#0%{IP}%22%%%0%-1%%%%%0%-1%0%%%0%0%0%0%%1080%%0%0%0#MobaFont%10%0%0%-1%15%236,236,236%30,30,30%180,180,192%0%-1%0%%xterm%-1%-1%_Std_Colors_0_%80%24%0%1%-1%<none>%%0#0# #-1\n')
    else: #Other Nodes have Telnet as the prefered method due to some software issues for now
        new_file.write(f'{node}=#129#1%{IP}%23%%%2%%%%%0%0%%1080%#MobaFont%10%0%0%-1%15%236,236,236%30,30,30%180,180,192%0%-1%0%%xterm%-1%-1%_Std_Colors_0_%80%24%0%1%-1%<none>%%0#0# #-1\n')

###############################
# For zte List
###############################
new_file.write('\n')
new_file.write('[Bookmarks_3]\n')
new_file.write('SubRep=ZTE\n')
new_file.write('ImgNum=41\n')

for d in range(0, df_zte.shape[0]):
    node = df_zte['ME Name'][d]
    IP = df_zte['IP Address'][d]    
    new_file.write(f'{node}=#129#1%{IP}%23%%%2%%%%%0%0%%1080%#MobaFont%10%0%0%-1%15%236,236,236%30,30,30%180,180,192%0%-1%0%%xterm%-1%-1%_Std_Colors_0_%80%24%0%1%-1%<none>%%0#0# #-1\n')

new_file.close()
print ("Script completed with success!!!")