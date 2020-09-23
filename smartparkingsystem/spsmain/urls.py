from django.urls import path
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token, verify_jwt_token

from .views import CreateUser, GetVacantSpot

urlpatterns = [
    path('user-register/', CreateUser.as_view()),
    path('token/', obtain_jwt_token, name='token_obtain_pair'),
    path('token/refresh/', refresh_jwt_token, name='token_refresh'),
    path('get-vaccant-spot/', GetVacantSpot.as_view()),
    path('api-token-verify/', verify_jwt_token),
]