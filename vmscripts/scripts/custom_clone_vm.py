from run_shell_command import *
from pgsql_conn import *
from generate_hex import *
import datetime
import pytz
from uuid import getnode as get_mac
import re
import libvirt
from manage_ip import *




#vmCloneCmd = "virt-clone --original vsusnjhhdevl001 --name " + vmName + " --file " + filePath + " --mac " + newMAC

imageFolderPath = "/var/kvm/images/"
xmlFolderPath = "/var/kvm/xmls/"

def getXMLPath(vmName):
  xmlPath = xmlFolderPath + vmName + ".xml"
  return xmlPath

def getImagePath(vmName):
  imagePath = imageFolderPath + vmName + ".img"
  return imagePath

  virsh dumpxml autoip4 > /var/kvm/xmls/newvm.xml

def copyVM(originalVm, vmName):
  originalVmPath = getImagePath(originalVm)
  newVmPath = getImagePath(vmName)
  vmCopyCommand = "cp " + originalVmPath + " " + newVmPath
  run_command(vmCopyCommand)

def configureXML(vmName, ramSize, noCPU, macAddr):
  xmlFile = getXMLPath(vmName)
  #Removing the UUID
  commandRemoveUUID = "perl -i -ne '/<uuid>/ or print'" + xmlFile
  run_command(commandRemoveUUID)
  print "Removed the UUID"
  # Edit the Ram Size
  commandEditVmName = 'perl -i -pe \'s/<name>[\s\S]*?<\/name>/<name>' + vmName + '<\/name>/g\'' + xmlFile
  commandEditRAMSize = 'perl -i -pe \'s/<memory unit='KiB'>[\s\S]*?<\/memory>/<memory unit="KiB">' + ramSize + '<\/memory>/g\'' + xmlFile
  commandEditCurrRAMSize = 'perl -i -pe \'s/<currentMemory unit="KiB">[\s\S]*?<\/currentMemory>/<currentMemory unit="KiB">' + ramSize + '<\/currentMemory>/g\'' + xmlFile
  #perl -i -pe 's/<mac\ address=[\s\S]*?\/>/<mac\ address=\"test macdata\"\/>/g' /var/kvm/xmls/newvm.xml
  commandEditMAC = 'perl -i -pe \'s/<mac\ address=[\s\S]*?\/>/<mac\ address=\"' + macAddr + '\"\/>/g' + xmlFile
  # <mac address='d8:50:e6:ba:c9:18'/>
  run_command(commandEditVmName)
  print "Edited Vmname"
  run_command(commandEditRAMSize)
  print "Edited RAM"
  run_command(commandEditCurrRAMSize)
  print "Edited Curr Ram"


# dump the xml for the original
#virsh dumpxml autoip4 > /var/kvm/xmls/newvm.xml

def createXML(originalVm, vmName):
  newVmXML = getXMLPath(vmName)
  createXMLCommand = "virsh dumpxml " + originalVm + " > " + newVmXML

def clone_vm(originalVm, vmName, ramSize, noCPU, macAddr):
  copyVM(originalVm, vmName)
  xmlFile = createXML(originalVm, vmName)
  configureXML(vmName, ramSize, noCPU, macAddr)
  print "VM cloned"
