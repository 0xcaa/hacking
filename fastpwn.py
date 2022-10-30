#!/usr/bin/python

from threading import Thread
from time import sleep, perf_counter
import subprocess
import sys


def subdomain(hostname, path, file):
    print("wfuzz", "-c", "-f", file+",raw", "-w", path+"/Discovery/DNS/bitquark-subdomains-top100000.txt", "-u", "http://"+hostname,"-H", "Host: FUZZ."+hostname, "--sc", "200,202,204,301,302,307,403")
    return  #remove

    dirb_out = subprocess.run(["wfuzz", "-c", "-f", file+",raw", "-w", path+"/Discovery/DNS/bitquark-subdomains-top100000.txt", "-u", "http://"+hostname,"-H", "Host: FUZZ."+hostname, "--sc", "200,202,204,301,302,307,403" ], stdout=subprocess.PIPE)
    out = dirb_out.stdout.decode("utf-8")

    # write to file
#    file_object = open(file, 'a')
#    file_object.write(out)
#    file_object.close()
    print("subdomain done!")

def dirbuster(hostname, path, file):
    print("wfuzz", "-f", file+",raw", "-w", "/Discovery/Web-Content/raft-large-directories.txt", "http://"+hostname+"/FUZZ/")
    return  #remove

    dirb_out = subprocess.run(["wfuzz", "-f", file+",raw", "-w", "/Discovery/Web-Content/raft-large-directories.txt", "http://"+hostname+"/FUZZ/"], stdout=subprocess.PIPE)
    out = dirb_out.stdout.decode("utf-8")

    # write to file
#    file_object = open(file, 'a')
#    file_object.write(out)
#    file_object.close()
    print("dirbuster done!")

def nmap(ip, flags, file):
    print("nmap -oN", file, flags, "ip")
    return  #remove

    nmap_out = subprocess.run(["nmap -oN", file, flags, "ip"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    out = nmap_out.stdout.decode("utf-8")

    # write to file
#    file_object = open(file, 'a')
#    file_object.write(out)
#    file_object.close()
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
    flags_nmap = ""
    nmap_file = "nmap_out.txt"
    dirb_file = "dirb_out.txt"
    subd_file = "subd_out.txt"

    with open('/etc/hosts') as f:
        if hostname not in f.read():
            f.close()
            print("hostname not in /etc/hosts file")
            sys.exit()



    if (q := input("run nmap?(y/n): ")) == "y":
        flags_nmap =  str(input("flags(blank for none): "))
        print("nmap started")
        t1 = Thread(target=nmap, args=(ip, flags_nmap, nmap_file))
        t1.daemon=True
        t1.start()
    elif q == "n":
        pass
    else:
        sys.exit()
    if (q := input("run dirb?(y/n): ")) == "y":
        print("dirb started")
        t2 = Thread(target=dirbuster, args=(ip, wlist_path, dirb_file))
        t2.start()
    elif q == "n":
        pass
    else:
        sys.exit()
    if (q := input("run subdomain brute?(y/n): ")) == "y":
        print("subdomain started")
        t3 = Thread(target=subdomain, args=(hostname, wlist_path, subd_file))
        t3.start()
    elif q == "n":
        pass
    else:
        sys.exit()

    t1.join()
    t2.join()
    t3.join()

    end_time = perf_counter()


    print(f'It took {end_time- start_time: 0.2f} second(s) to complete.')



if __name__ == "__main__":
    main()
