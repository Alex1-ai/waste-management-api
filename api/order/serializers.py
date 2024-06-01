from rest_framework import serializers
from .models import Trash
from ..account.serializers import UserSerializer


class TrashSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = Trash
        fields = ["id","user", "contact", "location","take_out_date","is_delivered", "updated_at"]
        read_only_fields = ['user']

