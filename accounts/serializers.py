from dataclasses import field, fields
from .models import *
from rest_framework import serializers

from django.utils.html import strip_tags
import datetime
from django.utils import timezone
from datetime import datetime
from accounts.models import CustomerInfo
from django.db.models import Q


from dataclasses import field
from accounts.models import *
from rest_framework import serializers, validators

