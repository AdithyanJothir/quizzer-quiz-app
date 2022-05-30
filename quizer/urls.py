"""quizer URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.urls import path,include
from quiz_view import views as quiz_views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('quiz_view.urls')),
    path('login/',quiz_views.login,name='login'),
    path('register/',quiz_views.register,name='register'),
    path('create_quiz/',quiz_views.create_quiz,name='create_quiz'),
    path('quiz/<url>',quiz_views.create_card,name='quiz'),
    path('create_card/',quiz_views.create_card,name='create_card'),
    path('logout/',LogoutView.as_view(template_name = 'quiz_view/login.html'),name='logout'),

]
