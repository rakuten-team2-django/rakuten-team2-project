from django.contrib import admin
from django.urls import path

from .auth import user_login, user_logout, user_signup
from .views import home, test_akiba, test_bibek, test_koya, test_yuto

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', home, name='home'),
    path('test_koya/',test_koya.as_view(), name='test_koya'),
    path('test_yuto/',test_yuto, name='test_yuto'),
    path('disc_items/',test_bibek, name='fetch_least_sold_items'),
    path('test_akiba/',test_akiba, name='test_akiba'),
    path('signup/', user_signup, name='signup'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('database_data/',test_bibek,name="database_data")
]
