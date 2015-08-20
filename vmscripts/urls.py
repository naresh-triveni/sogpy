from django.conf.urls import include, url
from vmscripts import v1
urlpatterns = [
  url(r'vmachines/list^$', v1.list_vms, name='list_vms'),
]