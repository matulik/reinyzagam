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
        print instance
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.save()
        return instance


class ArticleSerializer(serializers.Serializer):
    url = serializers.HyperlinkedIdentityField(view_name='article_detail', read_only=True)
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=500, required=True)
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), required=True)
    quantity = serializers.IntegerField(default=0, required=False, read_only=True)
    cost = serializers.DecimalField(decimal_places=2, max_digits=6, required=True)
    dateAdded = serializers.DateTimeField(default=timezone.now())
    whoAdded = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=False)

    def create(self, validated_data):
        # return Article.objects.create(**validated_data)
        name = validated_data.get('name')
        category = validated_data.get('category')
        cost = validated_data.get('cost')
        request = self.context['request']
        article = Article.add_article(name=name, categoryID=category.id, cost=cost, request=request)
        return article

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.category = validated_data.get('category', instance.category)
        instance.cost = validated_data.get('cost', instance.cost)
        instance.save()
        return instance

class ArticleUnitSerializer(serializers.Serializer):
    url = serializers.HyperlinkedIdentityField(view_name='articleunit_detail', read_only=True)
    id = serializers.IntegerField(read_only=True)
    location = serializers.PrimaryKeyRelatedField(queryset=Location.objects.all(), required=True)
    article = serializers.PrimaryKeyRelatedField(queryset=Article.objects.all(), required=True)
    order = serializers.PrimaryKeyRelatedField(queryset=Order.objects.all(), required=False)
    dateInserted = serializers.DateTimeField(default=timezone.now(), read_only=True)
    available = serializers.BooleanField(default=True, required=False)
    whoAdded = serializers.PrimaryKeyRelatedField(read_only=True)

    def create(self, validated_data):
        location = validated_data.get('location')
        article = validated_data.get('article')
        order = validated_data.get('order')
        available = validated_data.get('available')
        request = self.context['request']
        au = ArticleUnit.add_articleunit(location=location, article=article, order=order, dateInserted=timezone.now(), request=request)
        if order == True:
            au.set_available()
        elif order == False:
            au.set_unavailable()
        return au

    def update(self, instance, validated_data):
        location = validated_data.get('location')
        article = validated_data.get('article')
        order = validated_data.get('order')
        available = validated_data.get('available')
        request = self.context['request']
        if instance.available == True and available == False:
            instance.set_unavailable()
        elif instance.available == False and available == True:
            instance.set_available()
        if instance.order == None and order != None:
            instance.set_to_order(order.id)
        elif instance.order != None and order == None:
            instance.set_to_order(None)
        if location:
            instance.location = location
        if article:
            instance.article = article
        instance.save()
        return instance

class OrderSerializer(serializers.Serializer):
    url = serializers.HyperlinkedIdentityField(view_name='order_detail', read_only=True)
    id = serializers.IntegerField(read_only=True)
    cost = serializers.DecimalField(decimal_places=2, max_digits=6, default=0.00, read_only=True)
    discount = serializers.DecimalField(decimal_places=2, max_digits=6, default=0.00, required=False)
    dateOrder = serializers.DateTimeField(default=timezone.now(), read_only=True)
    dateSpend = serializers.DateTimeField(required=False, read_only=True)
    released = serializers.BooleanField(required=False, default=False)
    buyer = serializers.PrimaryKeyRelatedField(queryset=Buyer.objects.all())
    whoAdded = serializers.PrimaryKeyRelatedField(read_only=True)
    whoReleased = serializers.PrimaryKeyRelatedField(read_only=True)
    articles = ArticleUnitSerializer(source='get_articleunits', many=True, read_only=True)

    def create(self, validated_data):
        discount = validated_data.get('discount')
        released = validated_data.get('released')
        buyer = validated_data.get('buyer')
        request = self.context['request']
        order = Order.add_order(buyer, request)
        order.discount = discount
        if released:
            order.set_released(request)
        else :
            order.set_unreleased()
        order.recount_order()
        return order

    def update(self, instance, validated_data):
        discount = validated_data.get('discount')
        released = validated_data.get('released')
        buyer = validated_data.get('buyer')
        request = self.context['request']
        if discount:
            instance.discount = discount
        if buyer:
            instance.buyer = buyer
        if instance.released == True and released == False:
            instance.set_unreleased()
        elif instance.released == False and released == True:
            instance.set_released(request=request)

        instance.save()
        return instance


