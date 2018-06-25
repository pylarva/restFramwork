from rest_framework import serializers
from restful01 import models


class PagerSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Roles
        fields = "__all__"