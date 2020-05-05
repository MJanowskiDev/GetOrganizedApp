from django.urls import path
from authapp import views

app_name = 'auth_app'

urlpatterns = [
    path('login/', views.SiteLoginView.as_view(), name = 'login'),
    path('logout/', views.SiteLogoutView.as_view(), name = 'logout'),
    path('signup/', views.SignUpView.as_view(), name = 'signupuser' ),
]