from django.urls import re_path

from skrc.hostconf.views import wildcard_redirect

urlpatterns = [
    re_path('(?P<path>.*)', wildcard_redirect),
]
