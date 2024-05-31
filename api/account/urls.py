from rest_framework import routers
from django.urls import path, include


from . import views
from rest_framework_simplejwt.views import TokenRefreshView

# router = routers.DefaultRouter()
# router.register(r"", views.UserViewSet)

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.LoginAPIView.as_view(), name='login'),
    path('logout/', views.LogoutAPIView.as_view(), name='logout'),
    path('email-verify/', views.VerifyEmail.as_view(), name='email-verify'),
    path('token/refresh/',TokenRefreshView.as_view(), name='token_refresh'),
    path('request-reset-email/', views.RequestPasswordResetEmail.as_view(), name='request-reset-email'),
    path('password-reset/<uidb64>/<token>/', views.PasswordTokenCheckAPI.as_view(), name='password-reset-confirm'),
    path('password-reset-complete', views.SetNewPasswordAPIView.as_view(), name="password-reset-complete")

    # path('login/', views.signin, name='signin'),
    # path('logout/<int:id>/', views.signout, name='signout'),
    # path('', include(router.urls))
]