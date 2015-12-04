#coding=utf8

from Store.models import *
from rest_framework import serializers


class LocationSerializer(serializers.Serializer):
    url = serializers.HyperlinkedIdentityField(view_name='location_detail', read_only=True)
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=100, required=True)
    description = serializers.CharField(max_length=1000, allow_blank=True)

    def create(self, validated_data):
        return Location.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.save()
        return instance


class BuyerSerializer(serializers.Serializer):
    url = serializers.HyperlinkedIdentityField(view_name='buyer_detail', read_only=True)
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=100, required=True)
    firstName = serializers.CharField(max_length=50, required=False, allow_blank=True)
    surname = serializers.CharField(max_length=50, required=False, allow_blank=True)
    NIP = serializers.CharField(max_length=13, required=False, allow_blank=True)
    address = serializers.CharField(min_length=None, max_length=None, required=False, allow_blank=True)

    def create(self, validated_data):
        return Buyer.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.firstName = validated_data.get('firstName', instance.firstName)
        instance.surname = validated_data.get('surname', instance.surname)
        instance.NIP = validated_data.get('NIP', instance.NIP)
        instance.address = validated_data.get('address', instance.address)
        instance.save()
        return instance

class CategorySerializer(serializers.Serializer):
    url = serializers.HyperlinkedIdentityField(view_name='category_detail', read_only=True)
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=100, required=True)
    description = serializers.CharField(max_length=1000, required=False, allow_blank=True)

    def create(self, validated_data):
        return Category.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.save()
        return instance