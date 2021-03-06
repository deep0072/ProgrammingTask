from requests import request

from rest_framework.response import Response

from rest_framework_simplejwt.tokens import RefreshToken


from .serializers import LogoutSerializer, UserCreateSerializer, LoginSerializer,ChangePasswordSerializer
from rest_framework import generics, status

from rest_framework.permissions import IsAuthenticated
# from django.contrib.auth import login
from .models import User


class RegisterView(generics.GenericAPIView):
    serializer_class = UserCreateSerializer

    def post(self, request):
        user = request.data
        serializer = self.serializer_class(
            data=user
        )  # send request data from front end to serializer
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_data = serializer.data
        return Response(user_data, status=status.HTTP_201_CREATED)


class LoginApiView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):

        user = request.data
      

        serializer = self.serializer_class(data=user)
       

        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class ChangePasswordApiView(generics.UpdateAPIView):

    queryset = User.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = ChangePasswordSerializer




class LogoutApiView(generics.GenericAPIView):
    serializer_class = LogoutSerializer
    permission_classes = (IsAuthenticated,)

    def post(self,request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)








   