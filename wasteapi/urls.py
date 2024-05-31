"""
URL configuration for wasteapi project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
# from django.contrib import admin, include
# from django.urls import path
from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static
from django.conf import settings


admin.site.site_header = "Waste Management Admin"
admin.site.site_title = "Waste Management Admin Area"
admin.site.index_title = "Welcome to the Waste Management Admin Area"



from django.urls import re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi



schema_view = get_schema_view(
   openapi.Info(
      title="Waste Management API",
      default_version='v1',
      description="This is the documentation for the Waste Management System Api",
      terms_of_service="https://www.ourapp.com/policies/terms/",
      contact=openapi.Contact(email="contact@wastHr.local"),
      license=openapi.License(name="EDU License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('api/', include('api.urls')),
    # DOCUMENTATION CODE HERE
    # path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),


]

# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404='utils.views.error_404'
handler500='utils.views.error_500'