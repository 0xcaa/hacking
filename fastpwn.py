#!/usr/bin/python

from threading import Thread
from time import sleep, perf_counter
import subprocess
from subprocess import DEVNULL
import sys
import shlex



def subdomain(hostname, path, file):
    command = ["wfuzz"]
    command.append("-c")
    command.append("-f")
    command.append(file+",raw")
    command.append("-w")
    command.append(path+"/Discovery/DNS/bitquark-subdomains-top100000.txt")
    command.append("-u")
    command.append("http://"+hostname)
    command.append("-H")
    command.append("Host: FUZZ."+hostname)
    command.append("--sc")
    command.append("200,202,204,301,302,307,4032")
    command = shlex.join(command)
    print("dirb command: ", command)

    process =  subprocess.Popen(
            command,
            shell=True,
            stdout=DEVNULL,
            stderr=subprocess.STDOUT)

    print("subdomain PID: ", process.pid)
    return process.pid

def dirbuster(hostname, path, file):
    command = ["wfuzz"]
    command.append("-f")
    command.append(file+",raw")
    command.append("-w")
    command.append(path+"/Discovery/Web-Content/raft-large-directories.txt")
    command.append("http://"+hostname+"/FUZZ/")
    command = shlex.join(command)
    print("dirb command: ", command)

    process =  subprocess.Popen(
            command,
            shell=True,
            stdout=DEVNULL,
            stderr=subprocess.STDOUT)

    print("dirbuster PID: ", process.pid)

def nmap(ip, flags, file):
    command = ["nmap"]
    flags_list = shlex.split(flags)
    for i in flags_list:
        command.append(i)
    command.append("-oN")
    command.append(file)
    command.append(ip)
    command = shlex.join(command)
    print("nmap command: ",command)

    process =  subprocess.Popen(
            command,
            shell=True,
            stdout=DEVNULL,
            stderr=subprocess.STDOUT)
    print("nmap PID: ", process.pid)

def usage():
    print("USAGE\n")
    sleep(2)
    print(sys.argv[0], "<IP> <HOSTNAME> <Seclists path>")



def main():
    argc = len(sys.argv)
    if argc < 3:
        usage()
        sys.exit()

    ip = sys.argv[1]
    hostname = sys.argv[2]
    wlist_path = sys.argv[3]
    start_time = perf_counter()
    flags_nmap = ""
    nmap_file = "/home/sophist/nmap_out.txt"
    dirb_file = "/home/sophist/dirb_out.txt"
    subd_file = "/home/sophist/subd_out.txt"

    with open('/etc/hosts') as f:
        if hostname not in f.read():
            f.close()
            print("hostname not in /etc/hosts file")
            sys.exit()



    if (q := input("run nmap?(y/n): ")) == "y":
        flags_nmap =  str(input("flags(blank for none): "))
        print("nmap started")
        pid1 = nmap(ip, flags_nmap, nmap_file)
    if (q := input("run dirb?(y/n): ")) == "y":
        print("dirb started")
        pid2 = dirbuster(ip, wlist_path, dirb_file)
    if (q := input("run subdomain brute?(y/n): ")) == "y":
        print("subdomain started")
        pid3 = subdomain(hostname, wlist_path, subd_file)


    end_time = perf_counter()


    print(f'It took {end_time- start_time: 0.2f} second(s) to complete.')



if __name__ == "__main__":
    main()
