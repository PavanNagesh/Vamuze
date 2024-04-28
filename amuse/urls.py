"""
URL configuration for wefour project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from .import views
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views
from .views import user_profile, logout_view


urlpatterns = [
    path('signin', views.signin, name='signin'),
    path('login', views.user_login, name='login'),
    path('index', views.index, name='index'),
    path('innerpage', views.innerpage, name='innerpage'),
    path('portfolio', views.portfolio, name='portfolio'),
    path('home', views.home, name='home'),
    path('about', views.about, name='about'),
    path('contact', views.contact, name='contact'),
    path('header', views.header, name='header'),
    path('footer', views.footer, name='footer'),
    path('services', views.services, name='services'),
    path('userprofile/', user_profile, name='userprofile'),
    path('logout', logout_view, name='logout'),
    path('userprofile/change', views.change, name='change_email'),
    path('safety/', views.safety, name='safety'),
    path('rules', views.rules, name='rules'),
    path('update/', views.update, name='update'),
    path('change', views.change, name='changE'),
    path('userprofile/update', views.update, name='update'),
    
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
