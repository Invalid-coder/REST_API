from django.urls import path, include
from django.contrib import admin
from . import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='home'),
    path('about', views.about, name='about'),
    path('showlist/', views.index, name='showlist'),
]