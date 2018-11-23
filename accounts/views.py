from django.contrib.auth import authenticate, get_user_model
from django.db.models import Q
from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_jwt.settings import api_settings
from accounts.serializers import UserSignupSerializer
from accounts.permissions import NonAuthenticatedOnly


jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
jwt_response_payload_handler = api_settings.JWT_RESPONSE_PAYLOAD_HANDLER


User = get_user_model()


class LoginView(APIView):
    permission_classes = [NonAuthenticatedOnly]

    def post(self, request):
        if request.user.is_authenticated:
            return Response({
                "detail": "You are already authenticated"
            }, status=400)
        data = request.data
        username = data.get('username')  # username or email address
        password = data.get('password')
        # user = authenticate(username=username, password=password)
        qs = User.objects.filter(
            Q(username__iexact=username) |
            Q(email__iexact=username)
        ).distinct()
        if qs.count() == 1:
            user_obj = qs.first()
            if user_obj.check_password(password):
                user = user_obj
                payload = jwt_payload_handler(user)
                token = jwt_encode_handler(payload)
                response = jwt_response_payload_handler(token, user, request=request)
                return Response({"data": response})
        return Response({"detail": "Invalid credentials"}, status=401)


class SignupView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSignupSerializer
    permission_classes = [NonAuthenticatedOnly]

    def get_serializer_context(self):
        return {'request': self.request}



# class SignupView(APIView):
#     permission_classes = [permissions.AllowAny]
#
#     def post(self, request, *args, **kwargs):
#         if request.user.is_authenticated:
#             return Response({
#                 "detail": "You are already registered and are authenticated"
#             }, status=400)
#         data = request.data
#         username = data.get('username')
#         email = data.get('email')
#         password = data.get('password')
#         password2 = data.get('password2')
#
#         qs = User.objects.filter(
#             Q(username__iexact=username) |
#             Q(email__iexact=username)
#         )
#
#         if password != password2:
#             return Response({"password": "Password must match."}, status=401)
#         if qs.exists():
#             return Response({"detail": "This user already exists"}, status=401)
#         else:
#             user = User.objects.create(username=username, email=email)
#             user.set_password(password)
#             user.save()
#             payload = jwt_payload_handler(user)
#             token = jwt_encode_handler(payload)
#             response = jwt_response_payload_handler(token, user, request=request)
#             return Response({"data": response,
#                              "message": "User created successfully"}, status=201)
