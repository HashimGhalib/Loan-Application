from django.urls import path
from .views import Dashboard, SignUp, Home, AddBorrower, EditBorrower, DeleteBorrower, BorrowerProfile,\
    LoanApp, LoanAppDelete #, BorrowerView
from django.contrib.auth import views as auth_views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [

    #HOME-PAGE
    path('', Home.as_view(), name='home'),

    # DASHBOARD
    path('dashboard/', Dashboard.as_view(), name='dashboard'),

    # SIGNUP
    path('signup/', SignUp.as_view(), name='signup'),

    # LOGIN and LOGOUT
    path('login/', auth_views.LoginView.as_view(template_name='LoanView/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='LoanView/logout.html'), name='logout'),

    # BORROWER
    path('add-borrower/', AddBorrower.as_view(), name='add-borrower'),
    path('edit-borrower/<uuid:pk>/', EditBorrower.as_view(), name='edit-borrower'),
    path('delete-borrower/<uuid:pk>/', DeleteBorrower.as_view(), name='delete-borrower'),

    #BORROWE PROFILE
    path('borrower-profile/', BorrowerProfile.as_view(), name='borrower-profile'),

    # LOAN APPLICATION
    path('application/', LoanApp.as_view(), name='application'),
    path('delete-application/<uuid:pk>/', LoanAppDelete.as_view(), name='delete-application')

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

