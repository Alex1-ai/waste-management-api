from rest_framework import routers
from django.urls import path, include


from .import views

# router = routers.DefaultRouter()
# router.register(r"/candidates" ,views.CandidateViewSet)


urlpatterns = [
    path('', views.TrashListCreateView.as_view(), name="trash_take_out"),
    path('<int:pk>/', views.TrashDetailView.as_view(), name='trash-detail'),
    # path('candidate/', views.CandidateViewSet)
]