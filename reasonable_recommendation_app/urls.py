from django.contrib import admin
from django.urls import path

from .views import home, test_akiba, test_bibek, test_koya, test_yuto

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', home, name='home'),
    path('test_koya/',test_koya, name='test_koya'),
    path('test_yuto/',test_yuto, name='test_yuto'),
    path('test_bibek/',test_bibek, name='test_bibek'),
    path('test_akiba/',test_akiba, name='test_akiba'),
]
