from run_shell_command import *
from pgsql_conn import *
from generate_hex import *
import datetime
import pytz
from uuid import getnode as get_mac
import re
import libvirt
from manage_ip import *


# Increement the Last Hex of the MAC ID
def increementMACID(oldMAC, hostMAC):
  arrHostMAC = hostMAC.split(":")
  lastHostHEX = arrHostMAC[-1]
  if not oldMAC:
    lastHEX = arrHostMAC[-1]
    if lastHEX == '10':
      lastHEX = '11'
    else:
      lastHEX = '10'
    del arrHostMAC[-1]
    hostMAC = ":".join(arrHostMAC)
    return (hostMAC + ":" + lastHEX)
  else:
    arrOldMAC = oldMAC.split(":")
    lastHEX = arrOldMAC[-1]
    lastINT = int(lastHEX, 16)
    newLastINT = lastINT + 1
    newLastHEX = format(newLastINT, '02x')
    del arrOldMAC[-1]
    strOldMac = ":".join(arrOldMAC)
    return (strOldMac + ":" + newLastHEX)


#Create a MACID for the new VM.
def generateMAC(hostMAC):
  dbConn = create_connection('postgres', '127.0.0.1', 'postgres', 'postgres')
  lastMACID = select(dbConn, 'mac_lists', 'mac_id', "ORDER BY ID DESC  LIMIT 1")
  newMACID = hostMAC
  newMACID_check = True
  while (newMACID == hostMAC) or (newMACID_check):
    if lastMACID.__class__.__name__ == 'list' and len(lastMACID) != 0:
      print "Hello Testing line"
      print lastMACID
      lastMACID = lastMACID[0]['mac_id']
    newMACID = increementMACID(lastMACID, hostMAC)
    lastMACID = newMACID
    newMACID_check = select(dbConn, 'mac_lists', 'mac_id', " WHERE mac_id='{}'".format(newMACID))
  return newMACID


def convertHexMacInString(hexMac):
  hexMacArray = re.findall('..',hexMac)
  return (":".join(hexMacArray))


print "Cloning from vsusnjhhdevl001"


vmName = raw_input("Enter the VM name: ")
inputPassword = raw_input("Enter the root password for the VM: ")
hostName = raw_input("Enter the hostname of the VM: ")
#ipAddress = raw_input("Enter the ipAddress for VM: ")
#hostMAC = raw_input("Enter the MAC Address of host machine: ")

#GET IP ADDRESS 
ipAddress = get_free_ip()

#Get Mac Address
mac = get_mac()
macInHex = format(mac, '02x')
hostMAC = convertHexMacInString(macInHex)

#Clone a VM
#lastMACID = select(dbConn, 'mac_lists', '*', "ORDER BY ID DESC  LIMIT 1")
newMAC = generateMAC(hostMAC)

#Insert the new MAC in DB

print "New MAC ID : "
print newMAC

fileName = vmName + ".img"
imagePath = "/var/kvm/images/"
filePath = imagePath + fileName

#call(["virt-clone --original vsusnjhhdevl001 --name", vmName, " --file ", filePath])
vmCloneCmd = "virt-clone --original vsusnjhhdevl001 --name " + vmName + " --file " + filePath + " --mac " + newMAC

print "Cloning the VM"
run_command(vmCloneCmd)
print "VM cloned"



#Enable Customization on Cloned image

vmCustomizeCmd = "virt-sysprep --enable customize -a " + filePath
run_command(vmCustomizeCmd)
#call(["virt-sysprep --enable customize -a clon2.img"])

print "Changing the hostname"
vmHostnameCmd = "virt-sysprep -a " + filePath + "  --hostname " +  hostName
#call(["virt-sysprep -a clon2.img --hostname", hostName])

run_command(vmHostnameCmd)
print "Hostname Changed"

#Change hostname
# virt-sysprep -a clon2.img --hostname newhost


print "Changing the rootPassword"
rootPassword = "password:" + inputPassword
#Change root password
#call(["virt-sysprep --root-password", rootPassword , " -a clon2.img"])

vmRootpassCmd = "virt-sysprep --root-password " + rootPassword + " -a " + filePath

run_command(vmRootpassCmd)

print "Root Password changed"


#GET UUIDSTRING OF THE VM
conn=libvirt.open("qemu:///system")
dom = conn.lookupByName(vmName)
uuidString = dom.UUIDString()


#Inserting in DB 
dbConn = create_connection('postgres', '127.0.0.1', 'postgres', 'postgres')
mac_lists_id = insert (dbConn, 'mac_lists', {'mac_id' : newMAC, 'vm_uuid' : uuidString, 'created_at' : datetime.datetime.now(pytz.timezone("America/New_York")).strftime('%Y-%m-%d %H:%M:%S %z') })

allotIP(ipAddress, mac_lists_id)


## Assigning IP address 
# ipSetCmd = "echo -e \"DEVICE=eth0\nBOOTPROTO=static\nNETMASK=255.255.255.0\nGATEWAY=192.168.2.1\nDNS1=208.67.222.222\nDNS2=208.67.220.220\nONBOOT=yes\nHWADDR=" + newMAC + "\nIPADDR=" + ipAddress + "\" > /etc/sysconfig/network-scripts/ifcfg-eth0"

ipSetCmd = "echo -e \"TYPE=Ethernet\nBOOTPROTO=static\nDEFROUTE=yes\nPEERDNS=yes\nPEERROUTES=yes\nIPV4_FAILURE_FATAL=no\nIPV6INIT=yes\nIPV6_AUTOCONF=yes\nIPV6_DEFROUTE=yes\nIPV6_PEERDNS=yes\nIPV6_PEERROUTES=yes\nIPV6_FAILURE_FATAL=no\nNAME=eth0\nUUID=" + uuidString + "\nDEVICE=eth0\nONBOOT=yes\nIPADDR=" + ipAddress + "\nNETMASK=255.255.255.0\nGATEWAY=192.168.1.1\nDNS1=208.67.222.222\nDNS2=208.67.220.220\" > /etc/sysconfig/network-scripts/ifcfg-eth0"

vmIPSetCmd = "virt-sysprep -a " + filePath + " --run-command '" + ipSetCmd + "'"
run_command(vmIPSetCmd)

##Assigning IP address through DHCP 

#netUpdateCmd = "virsh net-update default add ip-dhcp-host \"<host name=\'" + vmName + "\' ip=\'" + ipAddress + "\' />\" --live --config"
#run_command(netUpdateCmd)

#virsh net-update default add ip-dhcp-host "<host name='clon2' ip='192.168.122.45' />" --live --config
