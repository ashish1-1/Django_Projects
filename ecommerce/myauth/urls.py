from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.mylogin, name='mylogin'),
    path('logout/', views.mylogout, name='mylogout'),
    path('activate/<uidb64>/<token>', views.activate, name='activate'),
    path('request-reset-email/',views.RequestResetEmailView.as_view(), name='request-reset-email'),
    path('reset/<uidb64>/<token>/',views.ResetPasswordView.as_view(), name='reset' )
]