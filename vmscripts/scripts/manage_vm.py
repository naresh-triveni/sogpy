import libvirt
import sys
import pprint

conn=libvirt.open("qemu:///system")
for id in conn.listDomainsID():
  dom = conn.lookupByID(id)
  info = dom.info()
  print "Name : ", dom.name()
  print "Id : ", id
  print "Info : ", info



vmId = raw_input("Enter the ID of the VM you need to manage : ")

selectedVM = conn.lookupByID(int(vmId))
print "Enter the following the code for changing the state of the selected VM."


print "1: run the VM "
print "2: suspend the VM "
print "3: resume the VM "
print "4: destroy the VM "
# print "5: shut off "
# print "6: crashed "

vmState = raw_input("Enter the State for the VM : ")


def f(selectedVM):
    return {
        '1': lambda res: selectedVM.create(),
        '2': lambda res: selectedVM.create(),
        '3': lambda res: selectedVM.create(),
        '4': lambda res: selectedVM.create(),
        '5': lambda res: selectedVM.create(),
    }[x]

if vmState == "1" :
  print selectedVM.create(),
elif vmState == "2" :
  print selectedVM.suspend(),
elif vmState == "3":
  print selectedVM.resume(),
elif vmState == "4":
  print selectedVM.destroy(),
else:
  print "Please enter a valid input"
