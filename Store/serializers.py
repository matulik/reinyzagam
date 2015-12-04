#coding=utf8

from Store.models import *
from rest_framework import serializers


class LocationSerializer(serializers.Serializer):
    url = serializers.HyperlinkedIdentityField(view_name='location_detail', read_only=True)
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=100, required=True)
    description = serializers.CharField(max_length=1000, required=False)

    def create(self, validated_data):
        return Location.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        return instance