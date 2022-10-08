from django.shortcuts import render
from requests import request

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.auth import AuthToken, TokenAuthentication
from .serializers import RegisterSerializer
from utils.custom_viewset import CustomViewSet
from utils.custom_permissions import *
from accounts.models import UserAccount
from knox.views import LoginView as KnoxLoginView
from rest_framework import permissions, status, viewsets

from django.utils import timezone
from drf_yasg2.utils import swagger_auto_schema
from django.contrib.auth import get_user_model, login
import random
from accounts.serializers import *
from cafe.serializers import Cafe
from utils.response_wrapper import ResponseWrapper

from django.contrib.auth.hashers import make_password

# Create your views here.


class LoginViewSet(CustomViewSet):
    queryset = Cafe.objects.all()
    lookup_field = 'pk'
