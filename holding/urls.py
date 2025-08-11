"""
URL configuration for holding project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from landing import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name="index"),
    path("servicios/", views.servicios, name="servicios"),
    path("equipo/", views.equipo, name="equipo"),
    path("blog/", views.blog, name="blog"),
    path('blog/<slug:slug>/', views.blog_detalles, name='blog_detalles'),
    path('etiqueta/<slug:slug>/', views.tag_detail, name='tag_detail'),
    path('guardar-cv/', views.guardar_cv, name='guardar_cv'),
    path('enviar-contacto/', views.enviar_contacto, name='enviar_contacto'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

