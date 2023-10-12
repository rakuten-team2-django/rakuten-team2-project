from django.contrib import admin
from django.urls import path

from .auth import user_login, user_logout, user_signup
from .views import test_akiba, test_bibek, Search_Reasonable, RankingSearch, Home, test_yuto
from .views_yuto import DiscountApplier

app_name = 'reasonable_recommendation_app'
urlpatterns = [
    path('admin/', admin.site.urls),
    path('search_reasonable/<int:page>',Search_Reasonable.as_view(), name='search_reasonable'),
    path('ranking_search/',RankingSearch.as_view(), name='ranking_search'),
    path('home/',Home.as_view(), name='home'),
    path('test_yuto/', DiscountApplier.as_view(), name='test_yuto'),
    path('disc_items/',test_bibek, name='fetch_least_sold_items'),
    path('test_akiba/',test_akiba, name='test_akiba'),
    path('signup/', user_signup, name='signup'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('database_data/',test_bibek,name="database_data")
]
