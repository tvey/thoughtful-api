from django.urls import path, include

from rest_framework_simplejwt.views import TokenRefreshView

from .views import register, MyTokenObtainPairView

app_name = 'users'

urlpatterns = [
    path('register/', register, name='register'),
    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
