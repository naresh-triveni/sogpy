from django.shortcuts import render_to_response
from django.http import HttpResponse
from vmscripts.scripts.listing_domains import list_virtual_machines
import json

def list_vms(request):
  virtual_machines = list_virtual_machines
  virtual_machines = json.dumps(virtual_machines)
  return HttpResponse(virtual_machines, content_type='application/json')

