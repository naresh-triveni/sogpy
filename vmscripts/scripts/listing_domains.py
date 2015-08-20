import libvirt
import sys
import pprint

def list_virtual_machines():
  conn=libvirt.open("qemu:///system")

  domain_dict_1 = []
  for id in conn.listDomainsID():
    dom = conn.lookupByID(id)
    info = dom.info()
    domain_dict_1.append({
      'name' : dom.name(),
      'info' : dom.info()
    })


  domain_dict_2 = []
  conn=libvirt.open("qemu:///system")
  for dom in conn.listAllDomains():
    info = dom.info()
    domain_dict_2.append({
      'name' : dom.name(),
      'info' : dom.info()
    })

  domain_dict = {
    'dict_1' : domain_dict_1,
    'dict_2' : domain_dict_2
  }
  return domain_dict

