from django.contrib import admin
from django.urls import path, re_path

from shorty.views import HomeView, SkrcRedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomeView.as_view(), name='home'),
    re_path('^(?P<shortcode>[a-zA-Z0-9]{6,15})/$', SkrcRedirectView.as_view(), name='shortcode')
]
