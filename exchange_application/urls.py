"""exchange_application URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from knox import views as knox_views
from exchange_application.views import LoginView, RegistrationAPI, ActivateAccountAPI
from django.conf import settings # new
from  django.conf.urls.static import static #new
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', RegistrationAPI.as_view()),
    path('activate/<str:activation_key>/', ActivateAccountAPI.as_view(), name='activate'),
    path('login/', LoginView.as_view(), name='knox_login'),
    path('logout/', knox_views.LogoutView.as_view(), name='knox_logout'),
    path('logoutall/', knox_views.LogoutAllView.as_view(), name='knox_logoutall'),
    path('hello/', views.hello, name='hello'),
    path('users/', include('users.urls')),
    path('student/', include('student.urls')),
    path('faculty/', include('faculty.urls')),
    path('ixo/', include('admin.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_URL)