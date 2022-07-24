from django.urls import path
from .views import RegisterView
from .import views

urlpatterns = [
    path('register/', RegisterView.as_view(), name="registerapi"),
    path('login/', views.getToken, name='getauthtoken'),
    path('superuserlogin/', views.getSuperuser, name='getsuperuser'),
]

