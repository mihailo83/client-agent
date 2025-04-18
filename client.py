import socket
import pickle
import os
import subprocess
import csv
import sys
import time
from datetime import datetime, timedelta


def applicaion(conf_file):
    if not os.path.exists(conf_file):
        ERR='CONFIG ERROR: file client.conf does not exist'
        return ERR
        
    client_hostname='None'
    server_address='None'
    server_port='None'
    schedule_time = None

    file1 = open(conf_file, 'r')

    for confLine in file1:
        if (confLine.find('hostname=') >=0) and (confLine[0:9]=='hostname='):
            client_hostname=confLine[9:-1]
        if (confLine.find('server_address=') >=0) and (confLine[0:15]=='server_address='):
            server_address=confLine[15:-1]
        if (confLine.find('server_port=') >=0) and (confLine[0:12]=='server_port='):
            server_port=int(confLine[12:-1])
        if confLine.startswith('schedule='):
            schedule_time = confLine[9:].strip()
    if client_hostname == 'None':
        ERR='CONFIG ERROR: "hostname" does not exist'
        return ERR
    if server_address == 'None':
        ERR='CONFIG ERROR: "server_address" does not exist'
        return ERR
    if server_port == 'None':
        ERR='CONFIG ERROR: "server_port" does not exist'
        return ERR
    
    connect_to_server(client_hostname,server_address,server_port)

    while schedule_time:
        try:
            now = datetime.now()
            target_time = datetime.strptime(schedule_time, "%H:%M").replace(
                year=now.year, month=now.month, day=now.day
            )
            if target_time <= now:
                target_time += timedelta(days=1)

            wait_seconds = (target_time - now).total_seconds()
            print(f"Waiting until {target_time.strftime('%H:%M')} (in {int(wait_seconds)} seconds)...")
            time.sleep(wait_seconds)
            connect_to_server(client_hostname, server_address, server_port)

        except ValueError:
            print(f"ERROR: Wrong time format in schedule: {schedule_time}. Use HH:MM.")
            break

    

def connect_to_server(client_hostname,server_address,server_port):
        data_list = collect_data(client_hostname)
        
        # print (data_list)
        print (f"Prepare for transfer: {str(len(data_list))}")
        
         # Сериализация списка
        data = pickle.dumps(data_list)
        
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((server_address, server_port))
                s.sendall(data)
                print("Transfer completed.")
        except ConnectionRefusedError:
            print(f"ERROR: server connection {server_address}:{server_port} refused.")
        except Exception as e:
            print(f"EXCEPTION ERROR: {e}")
      

def collect_data(client_hostname):
    result = []
    result.append('client_hostname='+ client_hostname)
    temp_file = 'temp.csv'

    # формируем список установленного по для х64
    if os.path.exists(temp_file):
        os.remove(temp_file)
    cmd1 = 'powershell.exe -command "Get-ItemProperty HKLM:\\Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\* | Select-Object DisplayName, DisplayVersion, Publisher, Size, InstallDate | Export-CSV temp.csv"'
    p = subprocess.Popen(cmd1, stdout=subprocess.PIPE, shell=True)
    res = p.communicate()[0]
    mes = res.decode('cp866')
    if os.path.exists(temp_file):
        # result = result + 'client_data_x64='
      
        with open(temp_file, newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')

            for row in reader: 
                if row[0]=='#TYPE Selected.System.Management.Automation.PSCustomObject': continue
                if (row[0]=='DisplayName') and (row[1] == 'DisplayVersion'): continue
                if row[0]=='': continue
                result.append('DisplayName='+ str(row[0]))
                if row[1] =='': 
                    result.append ('DisplayVersion=None')
                else: 
                    result.append ('DisplayVersion='+ str(row[1]))
        os.remove(temp_file)    

    # формируем список установленного по для х32
    if os.path.exists(temp_file):
        os.remove(temp_file)
    cmd1 = 'powershell.exe -command "Get-ItemProperty HKLM:\\SOFTWARE\\Wow6432Node\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\* | Select-Object DisplayName, DisplayVersion, Publisher, Size, InstallDate | Export-CSV temp.csv"'
    p = subprocess.Popen(cmd1, stdout=subprocess.PIPE, shell=True)
    res = p.communicate()[0]
    mes = res.decode('cp866')
    if os.path.exists(temp_file):
        with open(temp_file, newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            for row in reader:
                if row[0]=='#TYPE Selected.System.Management.Automation.PSCustomObject': continue
                if (row[0]=='DisplayName') and (row[1] == 'DisplayVersion'): continue
                if row[0]=='': continue
                result.append('DisplayName='+ str(row[0]))

                if row[1] =='': 
                    result.append ('DisplayVersion=None')
                else: 
                    result.append ('DisplayVersion='+ str(row[1]))
        os.remove(temp_file)    
    # формируем список установленного по для Windows Store
    if os.path.exists(temp_file):
        os.remove(temp_file)
    cmd1 = 'powershell.exe -command "Get-AppxPackage | Select Name, PackageFullName | Export-CSV temp.csv"'
    p = subprocess.Popen(cmd1, stdout=subprocess.PIPE, shell=True)
    res = p.communicate()[0]
    mes = res.decode('cp866')
    if os.path.exists(temp_file):
        with open(temp_file, newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            for row in reader:
                if row[0]=='#TYPE Selected.Microsoft.Windows.Appx.PackageManager.Commands.AppxPackage': continue
                if (row[0]=='Name') and (row[1] == 'PackageFullName'): continue
                if row[0]=='': continue
                result.append('DisplayName='+ str(row[0]))
                if row[1] =='': 
                    result.append ('DisplayVersion=None')
                else: 
                    result.append ('DisplayVersion='+ str(row[1]))              
        os.remove(temp_file)    
    return result

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("ERROR: Config file not found")
        sys.exit(1)

    config_path = sys.argv[1]
    conf_arr = applicaion(config_path)
    
    if conf_arr:
        print(conf_arr)






