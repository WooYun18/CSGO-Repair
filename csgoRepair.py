# CS:GO Repair
# A set of small tools to fix csgo issues like VAC incompatible etc.
# Author @WooYun
# Date 2022/4/4
import os

import psutil
import sys
import subprocess
import wmi
import win32com.client

# weather the process is running
def proc_exist(process_name):
    pl = psutil.pids()
    for pid in pl:
        # if the name of given process name equals to the existing process(pid)
        if psutil.Process(pid).name() == process_name:
            return pid
#get the process exe file path
def proc_path(process_name):
    for proc in psutil.process_iter():
        try:
            name = proc.name().lower()
            path = proc.exe()
        except psutil.AccessDenied:
            # print('Access denied. Launch csgoRepair in administrator.')
            continue
        if name == process_name:
            return path

def get_steam_path():
    steamflag = True
    # weather steam is running?
    while steamflag:
        if isinstance(proc_exist('steam.exe'), int):
            print('[CS:GO Repair] Steam is running. About to initialize Repair process.')
            steamflag = False
            steam_path = proc_path('steam.exe')
            return steam_path
        else:
            print('[CS:GO Repair] Can not find Steam running.')
            inputflag = input('Wanna retry? [Y/N]:')
            if (inputflag.strip(' ') == 'Y' or inputflag.strip(' ') == 'y'):
                steamflag = True
            else:
                steamflag = False
                sys.exit(0)

def repair_steam(steam_path):
    # use commands to repair steam serivces
    steam_path = steam_path.replace("\steam.exe","")
    steam_service_path = steam_path + '\\bin\\steamservice.exe'
    repair_command = '"' + steam_service_path + '"' + ' /repair'
    subprocess.run(repair_command)

def repair_dns():
    wmiservice = wmi.WMI()
    NicConfig = wmiservice.Win32_NetworkAdapterConfiguration(IPEnabled = True)
    if len(NicConfig) < 1:
        print('[CS:GO Repair] Failed to found working adapter.')
        exit()
    objNic = NicConfig[0]
    arrDNS = ['223.5.5.5','223.6.6.6']
    returnv = objNic.SetDNSServerSearchOrder(DNSServerSearchOrder=arrDNS)
    return returnv

def main():
    print('[CS:GO Repair] Welcome to csgoRepair.')
    steam_path = get_steam_path()
    #step1 calibrating steam services.
    os.system('title CS:GO Repair')
    print('[CS:GO Repair][1/5] Calibrating Steam Services.')
    repair_steam(steam_path)
    #step2 resetting LSP Services.
    os.system('title CS:GO Repair')
    print('[CS:GO Repair][2/5] Resetting LSP Services.')
    subprocess.run('netsh winsock reset')
    #step3 resetting launch options.
    os.system('title CS:GO Repair')
    print('[CS:GO Repair][3/5] Resetting game launch options.')
    subprocess.run('bcdedit /deletevalue nointegritychecks')
    subprocess.run('bcdedit /deletevalue loadoptions')
    subprocess.run('bcdedit /debug off')
    subprocess.run('bcdedit /deletevalue nx')
    #strp4 repair dns.
    os.system('title CS:GO Repair')
    print('[CS:GO Repair][4/5] Repairing DNS settings.')
    returnvalue = repair_dns()
    if returnvalue == 0:
        print('[CS:GO Repair] Failed to Repair DNS.')
    else:
        print('[CS:GO Repair] Successed repairing DNS.')
    #step4 repair os files.
    os.system('title CS:GO Repair')
    print('[CS:GO Repair][5/5] Repairing OS Files.')
    subprocess.run('sfc /scannow')
if __name__ == '__main__':
    main()