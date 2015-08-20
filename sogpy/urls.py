from django.conf.urls import include, url
from django.contrib import admin
from vmscripts import urls as vmscript_urls
urlpatterns = [
    # Examples:
    # url(r'^$', 'sogpy.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/v1/', include(vmscript_urls)),
]
