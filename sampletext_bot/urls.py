from django.conf.urls import url, include
from django.contrib import admin
from django.urls import path
from BotFunc import views


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^event/', views.event),
]
