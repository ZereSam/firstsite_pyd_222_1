
from django.urls import path

from authapp.views import login, logout
from bboard.views import IndexListView, by_rubric, BbCreateView

app_name = 'authapp'

urlpatterns = [
    path('login/', login, name='login'),
    path('logout', logout, name='logout')
    ]
