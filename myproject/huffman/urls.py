from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('encode/', views.encode, name='encode'),
    path('decode/', views.decode, name='decode'),
    path('downloadEn',views.downloadEn,name='downloadEn'),
     path('downloadDe',views.downloadDe,name='downloadDe')
]
if settings.DEBUG:  # Serve media files during development
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
