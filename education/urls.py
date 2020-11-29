from django.contrib import admin
from django.urls import path
from . import views
from django.contrib.staticfiles.urls import static
from task import settings
urlpatterns = [
    path('', views.home,name='home'),
    path("search/", views.search, name="Search"),
    path('login/', views.handleLogin,name='login'),
    path('logout/', views.handleLogout,name='logout'),
    path('signup/', views.signup,name='signup'),

]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
