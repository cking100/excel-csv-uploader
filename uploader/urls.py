from django.urls import path
from .views import upload_file, home, login_view, logout_view

urlpatterns = [
    path('', home, name='home'),
    path('upload/', upload_file, name='upload_file'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
]
