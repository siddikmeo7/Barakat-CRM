<<<<<<< HEAD

from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include("django.contrib.auth.urls")),
    path('',include('accounts.urls')),
    path('nur/',include('Nur.urls')),
]
=======

from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
]
>>>>>>> 9aa85693653fbdaefe6c176d01c65fab7899ae95
