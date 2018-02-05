"""myproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.urls import path
from django.conf.urls.static import static
from myboke import views
from . import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('base/', views.base),
    path('register/', views.register),
    path('info/', views.info),
    path('login/', views.login),
    path('create/', views.create),
    path('logout/', views.logout),

    path('index/', views.index),
    path('article/', views.article),
    path('comment/', views.comment),
    path('editor/', views.editor),
    path('search/', views.search),
    path('delete/', views.delete),
    path('change_icon/',views.change_icon)
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

