import email
from django.shortcuts import render
from requests import request

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.auth import AuthToken, TokenAuthentication
from .serializers import *
from utils.custom_viewset import CustomViewSet
from accounts.models import UserAccount
from knox.views import LoginView as KnoxLoginView
from rest_framework import permissions, status, viewsets

from django.utils import timezone
from drf_yasg2.utils import swagger_auto_schema
from django.contrib.auth import get_user_model, login
import random
from accounts.serializers import *
from utils.response_wrapper import ResponseWrapper

from django.contrib.auth.hashers import make_password

# Create your views here.


class UserAccountViewSet(CustomViewSet):
    queryset = UserAccount.objects.all()
    lookup_field = 'pk'

    def get_serializer_class(self):
        if self.action == 'login':
            self.serializer_class = AuthTokenSerializer

        elif self.action == 'register':
            self.serializer_class = RegisterSerializer

        return self.serializer_class

    def get_permissions(self):
        permission_classes = []
        if self.action in ["user_update", "user_details"]:
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [permissions.AllowAny]
        return [permission() for permission in permission_classes]


    def register(self, request, *args, **kwargs):
        password = request.data.pop("password")
        email = request.data["email"]
        phone = request.data["phone"]
        verification_id = uuid.uuid4().__str__()

        email_exist = UserAccount.objects.filter(email=email).exists()

        if email_exist:
            return ResponseWrapper(
                error_msg="Email is Already Found", status=400
            )

        phone_exist = UserAccount.objects.filter(phone=phone).exists()

        if phone_exist:
            return ResponseWrapper(
                error_msg="Phone Number is Already Found", status=400
            )
        try:
            password = make_password(password=password)
            user = UserAccount.objects.create(
                password=password,
                **request.data
            )
            _, token = AuthToken.objects.create(user)

        except Exception as err:
            # logger.exception(msg="error while account creation")

            return ResponseWrapper(
                error_msg="Account Can't Create", status=400
            )

        serializer = UserDetailsSerializer(instance=user)

        context = {
            'user_info': serializer.data,
            'token': token,
        }
        return ResponseWrapper(data=context, status=200)


    def login(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')

        if not username:
            return ResponseWrapper(error_msg='User Name is Not Given', status=400)

        if not password:
            return ResponseWrapper(error_msg='Password is Not Given', status=400)

        qs = UserAccount.objects.filter(Q(phone=username)| Q(email=username)
                                        ).last()

        if not qs:
            return ResponseWrapper(error_msg='User Not Found', status=400)

        elif qs.check_password(password):
            _, token = AuthToken.objects.create(qs)
            serializer = UserDetailsSerializer(instance=qs)

            context = {
                'user_info': serializer.data,
                'token': token,
            }
            return ResponseWrapper(data=context, status=200)

        return ResponseWrapper(error_msg="Password Doesn't Match", status=400)


    def user_details(self, request, *args, **kwargs):
        qs = UserAccount.objects.filter(email=self.request.user).last()

        if not qs:
            return ResponseWrapper(error_msg='User Not Found',
                                   error_code=400)

        serializer = UserDetailsSerializer(instance=qs)
        _, token = AuthToken.objects.create(qs)

        context = {
            "user_info": serializer.data,
            'token': token,
        }

        return ResponseWrapper(data=context, status=200)

