from django.urls import path
from .views import RegisterUser, Dashboard, LogoutUser,LoginUser

app_name = 'account'

urlpatterns = [
    path('register/', RegisterUser.as_view(), name='register_user'),
    path('login/', LoginUser.as_view(), name='login_user'),
    path('dashboard/', Dashboard.as_view(), name='dashboard'),
    path('logout/', LogoutUser.as_view(), name='user_logout'),
]
