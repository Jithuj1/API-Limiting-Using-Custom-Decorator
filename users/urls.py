from django.urls import path
from .views import UserDetails, ListUser,  MytokenObtainPairView
from rest_framework_simplejwt.views import(TokenRefreshView)


urlpatterns = [
    path('api/token/', MytokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('users', UserDetails),
    path('list_users', ListUser),
]
