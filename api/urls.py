from django.urls import path, include
from rest_framework.authtoken import views
from .views import home


urlpatterns = [
    path('', home, name='api.home'),
    path('auth/', include('api.account.urls')),
    path('trash/', include('api.order.urls')),


]