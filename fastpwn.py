#!/usr/bin/python

from threading import Thread
from time import sleep, perf_counter
import subprocess
import sys


def subdomain(hostname, path, file):
    print("hello from subdomain")

    dirb_out = subprocess.run(["wfuzz", "-c", "-f", file, "-w", path+"/Discovery/DNS/bitquark-subdomains-top100000.txt", "-u", "http://"+hostname,"-H", "Host: FUZZ."+hostname, "--sc", "200,202,204,301,302,307,403" ], stdout=subprocess.PIPE)
    out = dirb_out.stdout.decode("utf-8")

    # write to file
    file_object = open(file, 'a')
    file_object.write(out)
    file_object.close()
    print("subdomain done!")

def dirbuster(hostname, path, file):

    print("hello from dirbuster")

    dirb_out = subprocess.run(["wfuzz", "-w", path+"/Discovery/Web-Content/raft-large-directories.txt", "http://"+hostname+"/FUZZ/"], stdout=subprocess.PIPE)
    out = dirb_out.stdout.decode("utf-8")

    # write to file
    file_object = open(file, 'a')
    file_object.write(out)
    file_object.close()
    print("dirbuster done!")

def nmap(ip, file):
    print("hello from nmap")

    nmap_out = subprocess.run(["nmap", "ip"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    out = nmap_out.stdout.decode("utf-8")

    # write to file
    file_object = open(file, 'a')
    file_object.write(out)
    file_object.close()
    print("nmap done!")


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
    nmap_file = "nmap_out.txt"
    dirb_file = "dirb_out.txt"
    subd_file = "subd_out.txt"

    with open('/etc/hosts') as f:
        if hostname not in f.read():
            f.close()
            print("hostname not in /etc/hosts file")
            sys.exit()

    t1 = Thread(target=nmap, args=(ip, nmap_file))
    t2 = Thread(target=dirbuster, args=(ip, wlist_path, dirb_file))
    t3 = Thread(target=subdomain, args=(hostname, wlist_path, subd_file))

    t1.start()
    t2.start()
    t3.start()

    t1.join()
    t2.join()
    t3.join()

    end_time = perf_counter()


    print(f'It took {end_time- start_time: 0.2f} second(s) to complete.')



if __name__ == "__main__":
    main()
