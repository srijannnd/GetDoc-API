from django.contrib.auth import authenticate, get_user_model
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_jwt.settings import api_settings

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER


class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        if request.user.is_authenticated:
            return Response({
                "detail": "You are already authenticated"
            }, status=400)
        data = request.data
        username = data.get('username')
        password = data.get('password')
        user = authenticate(username=username, password=password)
        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)
        return Response({'token': token})

