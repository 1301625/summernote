from django.urls import path
from . import views
urlpatterns= [
    path('signup', views.signup, name='signup'),
    path('login/', views.log_in, name='login'),
    path('logout', views.log_out, name='logout'),
    path('create', views.UserRegistrationView.as_view() , name='create'),
    path('<int:pk>/verify/<token>/' , views.UserVerificationView.as_view()),
    path('resend_verify_email', views.ResendVerifyEmailView.as_view() , name='resend'),
]