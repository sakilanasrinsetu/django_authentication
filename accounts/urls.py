from django.urls import path

from .views import *

urlpatterns =[
    path('register/',
         UserAccountViewSet.as_view({'post': 'register'}, name='register')),

    path('login/',
         UserAccountViewSet.as_view({'post': 'login'}, name='login')),
    
    path('user_details/',
         UserAccountViewSet.as_view({'get': 'user_details'}, name='user_details')),
]