from django.urls import path
from .views import signup_view, activate, login_view

urlpatterns = [
    path('signup/', signup_view, name='signup'),
    path('activate/<uidb64>/<token>/', activate, name='activate'),
    path('login/', login_view, name='login'),
    
]