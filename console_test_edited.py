import subprocess
import csv
import sys
import time

#Getting serial number of ASA device from user input
serial_num = input("Enter Serial Number: ")

with open('parameters.csv',newline='') as csvfile:
    reader = csv.reader(csvfile)
    found = 0
	#looping through parameters.csv to find record matching provided serial number
    for row in reader:
        if row[0]==serial_num:
            found = 1
            print("FOUND!....",row)

            hostname = row[1]
            outside_ip = row[2]
            inside_ip = row[3]
            gateway_ip = row[4]
            mgmt_ip = row[5]
            break

    if not found:
        print("Serial number was not found in csv... Please re-run this script to try again")
        sys.exit()

print("Calling subprocess...")
#Creating screen session to consoled device
subprocess.call(["screen","-d","-m","-S","cisco2","/dev/ttyUSB0"])
#applying hostname to device and starting session with sfr module
subprocess.call(["screen","-S","cisco2","-X","stuff","no\r\ren\r\rconf t\rhostname "+hostname+"\rexit\rsession sfr console\r"],stdout=subprocess.PIPE)
time.sleep(15)
#logging in as admin
subprocess.call(["screen","-S","cisco2","-X","stuff","\r\radmin\r"],stdout=subprocess.PIPE)
time.sleep(2)
#providing default admin password
subprocess.call(["screen","-S","cisco2","-X","stuff","Admin123\r"],stdout=subprocess.PIPE)
time.sleep(10)
#return to start EULA agreement
subprocess.call(["screen","-S","cisco2","-X","stuff","\r"],stdout=subprocess.PIPE)
time.sleep(2)
#skipping scroll through EULA agreement
subprocess.call(["screen","-S","cisco2","-X","stuff","q"],stdout=subprocess.PIPE)
time.sleep(2)
#agreeing to EULA agreement
subprocess.call(["screen","-S","cisco2","-X","stuff","YES\r"],stdout=subprocess.PIPE)
time.sleep(2)
#providing new password to sfr module
subprocess.call(["screen","-S","cisco2","-X","stuff","C1sc0123\rC1sc0123\r"],stdout=subprocess.PIPE)
time.sleep(10)
#accepting default config values
subprocess.call(["screen","-S","cisco2","-X","stuff","\r\r\r"],stdout=subprocess.PIPE)
time.sleep(1)
#providing mgmt IP to sfr module
subprocess.call(["screen","-S","cisco2","-X","stuff",""+mgmt_ip+"\r"],stdout=subprocess.PIPE)
time.sleep(1)
#providing subnet value for sfr module
subprocess.call(["screen","-S","cisco2","-X","stuff","255.255.255.0\r"],stdout=subprocess.PIPE)
time.sleep(1)
#providing gateway IP for sfr module
subprocess.call(["screen","-S","cisco2","-X","stuff",""+gateway_ip+"\r"],stdout=subprocess.PIPE)
time.sleep(1)
#providing DNS IP for sfr module
subprocess.call(["screen","-S","cisco2","-X","stuff","\r8.8.8.8\r"],stdout=subprocess.PIPE)
time.sleep(1)
#providing domain name for sfr module
subprocess.call(["screen","-S","cisco2","-X","stuff","cisco.com\r"],stdout=subprocess.PIPE)
time.sleep(1)
#accepting agreeing to complete initial setup
subprocess.call(["screen","-S","cisco2","-X","stuff","\r\r"],stdout=subprocess.PIPE)
time.sleep(160)
#configuring IP of FMC manager device to register with
subprocess.call(["screen","-S","cisco2","-X","stuff","configure manager add 192.168.10.20 C1sc0123\r"],stdout=subprocess.PIPE)

#output = process.communicate()[0]
#output.stdout.decode('utf-8')
#print(format(output))