"""wavepool URL Configuration
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from wavepool import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.front_page, name='home'),
    path('instructions/', views.instructions, name='instructions'),
    path('news/<int:newspost_id>/', views.newspost_detail, name='newspost_detail')
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
