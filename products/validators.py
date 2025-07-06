from rest_framework import serializers
from rest_framework import validators

from .models import Products

def validate_price(value):
    if value == 69.00:
        raise serializers.ValidationError("Not that pose...")
    return value

validate_title = validators.UniqueValidator(queryset=Products.objects.all(), lookup='iexact')