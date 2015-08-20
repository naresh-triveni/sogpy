import xml.etree.cElementTree as ET

vmName = raw_input("Name of the VM : ")
memorySize = raw_input("Memory Size of VM : ")
vcpu = raw_input("No of processor : ")

root = ET.Element("domain", type="kvm")
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

devices = ET.SubElement(root, "devices")
devicesEmulator = ET.SubElement(devices, "emulator").text = "/usr/libexec/qemu-kvm"
devicesDisk = ET.SubElement(devices, "disk", type='file', device='disk')
devicesDiskDriver = ET.SubElement(devicesDisk, "driver", name='qemu', type='raw', cache='none', io='threads')
devicesDiskSource = ET.SubElement(devicesDisk, "driver", file='/tmp/centos7/CentOS-7-x86_64-Everything-1503-01.iso')
devicesDiskTarget = ET.SubElement(devicesDisk, "target", dev='vda', bus='virtio')
devicesDiskSharable = ET.SubElement(devicesDisk, "shareable")

devicesSerial = ET.SubElement(devices, "serial", type='pty')
devicesSerialTaget = ET.SubElement(devicesSerial, "target", port='0')
devicesConsole = ET.SubElement(devices, "console", type='pty')
devicesConsoleTaget = ET.SubElement(devicesConsole, "target", type='serial', port='0')


tree = ET.ElementTree(root)
tree.write("new_domain.xml")
