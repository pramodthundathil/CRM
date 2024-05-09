from django.contrib import admin
from django.urls import path, include 
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path("",include("Home.urls")),
    path("transactions/",include("transactions.urls")),
    path("contacts/",include('Contacts.urls')),
   
    
]
urlpatterns += static(settings.MEDIA_URL , document_root = settings.MEDIA_ROOT)