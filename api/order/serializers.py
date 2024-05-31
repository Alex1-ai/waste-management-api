from rest_framework import serializers
from .models import Trash



class TrashSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trash
        fields = ["id","user", "contact", "location","take_out_date", "updated_at"]
        read_only_fields = ['user']

