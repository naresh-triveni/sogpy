import libvirt
conn_handler = libvirt.open("qemu:///system") 
f=open("/home/edevadmin/scripts/sample_xml/working_nav.xml")
xml=f.read() 
xml
dom_ref=conn_handler.defineXML(xml)
conn_handler.listDefinedDomains()
dom_ref.create()
