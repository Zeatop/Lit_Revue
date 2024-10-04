from django.urls import path
from .views import MyLoginView, RegisterView
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy

app_name = 'users'

urlpatterns = [
    path('login/', MyLoginView.as_view(),name='login'),
    path('logout/', auth_views.logout_then_login, {'login_url': reverse_lazy('users:login')}, name='logout'),
    # next_page est l'argument qui définit l'url vers laquelle on sera redirigé
    path('register/', RegisterView.as_view(),name='register'),                                  
]
