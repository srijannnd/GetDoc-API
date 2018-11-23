from django.urls import path
from rest_framework_jwt.views import refresh_jwt_token, obtain_jwt_token
from accounts.views import *


urlpatterns = [
    path('login/', LoginView.as_view()),
]