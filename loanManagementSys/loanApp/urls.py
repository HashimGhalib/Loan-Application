from django.urls import path
from .views import Dashboard, SignUp, Home
from django.contrib.auth import views as auth_views

urlpatterns = [

    #HOME-PAGE
    path('', Home.as_view(), name='home'),

    # DASHBOARD
    path('/dashboard', Dashboard.as_view(), name='dashboard'),

    # SIGNUP
    path('signup/', SignUp.as_view(), name='signup'),

    # LOGIN and LOGOUT
    path('login/', auth_views.LoginView.as_view(template_name='LoanView/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='LoanView/logout.html'), name='logout'),
]

