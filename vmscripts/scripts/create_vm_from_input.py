import xml.etree.cElementTree as ET
import libvirt
from pgsql_conn import *
import datetime
import pytz

dbConn = create_connection('postgres', '127.0.0.1', 'postgres', 'postgres')

vmName = raw_input("Name of the VM : ")
memorySize = raw_input("Memory Size of VM : ")
vcpu = raw_input("No of processor : ")
from random import randint
vmID = randint(1,500) 
print "Alloted Id will be : ", vmID

root = ET.Element("domain", type="kvm", id=str(vmID))
name = ET.SubElement(root, "name").text = vmName
memory = ET.SubElement(root, "memory", unit="KiB").text = memorySize
currentMemory = ET.SubElement(root, "currentMemory", unit="KiB").text = memorySize
vcpu = ET.SubElement(root, "vcpu").text = vcpu

os = ET.SubElement(root, "os")
osType = ET.SubElement(os, "type", arch="x86_64").text = "hvm"
osBoot = ET.SubElement(os, "boot", dev="hd")
features = ET.SubElement(root, "features")
featuresACPI = ET.SubElement(features, "acpi")
featuresAPIC = ET.SubElement(features, "apic")
featuresPAE = ET.SubElement(features, "pae")

clock = ET.SubElement(root, "clock", offset='utc')
onPoweroff = ET.SubElement(root, "on_poweroff").text = "destroy"
onReboot = ET.SubElement(root, "on_reboot").text = "destroy"
onCrash = ET.SubElement(root, "on_crash").text = "destroy"

serial = ET.SubElement(root, "serial", type='pty')
serialTaget = ET.SubElement(serial, "target", port='0')
console = ET.SubElement(root, "console", type='pty')
consoleTaget = ET.SubElement(console, "target", type='serial', port='0')

devices = ET.SubElement(root, "devices")
devicesEmulator = ET.SubElement(devices, "emulator").text = "/usr/libexec/qemu-kvm"
devicesDisk = ET.SubElement(devices, "disk", type='file', device='disk')
devicesDiskDriver = ET.SubElement(devicesDisk, "driver", name='qemu', type='raw', cache='none', io='threads')
devicesDiskSource = ET.SubElement(devicesDisk, "source", file='/tmp/centos7/CentOS-7-x86_64-Everything-1503-01.iso')
devicesDiskTarget = ET.SubElement(devicesDisk, "target", dev='vda', bus='virtio')
devicesDiskSharable = ET.SubElement(devicesDisk, "shareable")

devicesSerial = ET.SubElement(devices, "serial", type='pty')
devicesSerialTaget = ET.SubElement(devicesSerial, "target", port='0')
devicesConsole = ET.SubElement(devices, "console", type='pty')
devicesConsoleTaget = ET.SubElement(devicesConsole, "target", type='serial', port='0')


tree = ET.ElementTree(root)
tree.write("/home/edevadmin/templates/new_domain"+str(vmID)+".xml")

templateFilePath = "/home/edevadmin/templates/new_domain"+str(vmID)+".xml"

conn_handler = libvirt.open("qemu:///system") 
f=open("/home/edevadmin/templates/new_domain"+str(vmID)+".xml")
xml=f.read() 
#xml
dom_ref=conn_handler.defineXML(xml)
conn_handler.listDefinedDomains()
dom_ref.create()

print "Inserting the VM Detail in DB"

insert (dbConn, 'vms', {'domain_name' : vmName, 'memory_size' : memorySize, 'vcpu' : vcpu, 'alloted_vm_id' : vmID, 'vm_id' : vmID, 'template_xml_file' : templateFilePath, 'start_time' : datetime.datetime.now(pytz.timezone("America/New_York")).strftime('%Y-%m-%d %H:%M:%S %z') })


