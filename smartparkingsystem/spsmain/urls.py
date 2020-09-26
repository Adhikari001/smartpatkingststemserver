from django.urls import path
from rest_framework_jwt.views import obtain_jwt_token

from .views import CreateUser, GetVacantSpot, ReserveSpot

urlpatterns = [
    path('user/user-register/', CreateUser.as_view()),
    path('user/token/', obtain_jwt_token, name='token_obtain_pair'),
    path('parking/get-vaccant-spot/', GetVacantSpot.as_view()),
    path('parking/reserve-spot/', ReserveSpot.as_view()),
]