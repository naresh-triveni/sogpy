import xml.etree.ElementTree as ET

def get_element():
  tree = ET.parse('test.xml')
  root = tree.getroot()
  print root.iter('rpm')

get_element()
