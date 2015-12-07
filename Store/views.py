#coding=utf8

from django.shortcuts import render

from django.shortcuts import render, render_to_response, RequestContext, redirect

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from User.models import Login

from Store.models import *
from Store.serializers import *


# Location
@api_view(['GET', 'POST'])
def locations_list(request):
    if not Login.auth(request):
        msg = u'You are logged out. Please login first.'
        return render_to_response('login.html', { 'msg': msg }, context_instance=RequestContext(request))
    else:
        # Dla metody GET - pobierz listę
        if request.method == 'GET':
            locs = Location.objects.all()
            serializer = LocationSerializer(locs, context={'request': request}, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        # Dla metody POST - Utwórz nowego użytkownika
        if request.method == 'POST':
            serializer = LocationSerializer(context={'request': request}, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def location_detail(request, pk):
    if not Login.auth(request):
        msg = u'You are logged out. Please login first.'
        return render_to_response('login.html', { 'msg': msg }, context_instance=RequestContext(request))
    else:
        try:
            loc = Location.objects.get(id=pk)
        except Location.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if request.method == 'GET':
            serializer = LocationSerializer(loc, context={'request': request})
            return Response(serializer.data)

        if request.method == 'PUT':
            serializer = LocationSerializer(loc, context={'request': request}, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        if request.method == 'DELETE':
            loc.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

# Buyer
@api_view(['GET', 'POST'])
def buyers_list(request):
    if not Login.auth(request):
        msg = u'You are logged out. Please login first.'
        return render_to_response('login.html', { 'msg': msg }, context_instance=RequestContext(request))
    else:
        # Dla metody GET - pobierz listę
        if request.method == 'GET':
            buyers = Buyer.objects.all()
            serializer = BuyerSerializer(buyers, context={'request': request}, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        # Dla metody POST - Utwórz nowego użytkownika
        if request.method == 'POST':
            serializer = BuyerSerializer(context={'request': request}, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def buyer_detail(request, pk):
    if not Login.auth(request):
        msg = u'You are logged out. Please login first.'
        return render_to_response('login.html', { 'msg': msg }, context_instance=RequestContext(request))
    else:
        try:
            buyer = Buyer.objects.get(id=pk)
        except Buyer.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if request.method == 'GET':
            serializer = BuyerSerializer(buyer, context={'request': request})
            return Response(serializer.data)

        if request.method == 'PUT':
            serializer = BuyerSerializer(buyer, context={'request': request}, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        if request.method == 'DELETE':
            buyer.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

# Category
@api_view(['GET', 'POST'])
def categories_list(request):
    if not Login.auth(request):
        msg = u'You are logged out. Please login first.'
        return render_to_response('login.html', { 'msg': msg }, context_instance=RequestContext(request))
    else:
        # Dla metody GET - pobierz listę
        if request.method == 'GET':
            cat = Category.objects.all()
            serializer = CategorySerializer(cat, context={'request': request}, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        # Dla metody POST - Utwórz nowego użytkownika
        if request.method == 'POST':
            serializer = CategorySerializer(context={'request': request}, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def category_detail(request, pk):
    if not Login.auth(request):
        msg = u'You are logged out. Please login first.'
        return render_to_response('login.html', { 'msg': msg }, context_instance=RequestContext(request))
    else:
        try:
            cat = Category.objects.get(id=pk)
        except Category.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if request.method == 'GET':
            serializer = CategorySerializer(cat, context={'request': request})
            return Response(serializer.data)

        if request.method == 'PUT':
            serializer = CategorySerializer(cat, context={'request': request}, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        if request.method == 'DELETE':
            cat.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

# Article
@api_view(['GET', 'POST'])
def articles_list(request):
    if not Login.auth(request):
        msg = u'You are logged out. Please login first.'
        return render_to_response('login.html', { 'msg': msg }, context_instance=RequestContext(request))
    else:
        # Dla metody GET - pobierz listę
        if request.method == 'GET':
            art = Article.objects.all()
            serializer = ArticleSerializer(art, context={'request': request}, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        # Dla metody POST - Utwórz nowego użytkownika
        if request.method == 'POST':
            serializer = ArticleSerializer(context={'request': request}, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def article_detail(request, pk):
    if not Login.auth(request):
        msg = u'You are logged out. Please login first.'
        return render_to_response('login.html', { 'msg': msg }, context_instance=RequestContext(request))
    else:
        try:
            art = Article.objects.get(id=pk)
        except Article.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if request.method == 'GET':
            serializer = ArticleSerializer(art, context={'request': request})
            return Response(serializer.data)

        if request.method == 'PUT':
            serializer = ArticleSerializer(art, context={'request': request}, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        if request.method == 'DELETE':
            art.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

# Order
@api_view(['GET', 'POST'])
def orders_list(request):
    if not Login.auth(request):
        msg = u'You are logged out. Please login first.'
        return render_to_response('login.html', { 'msg': msg }, context_instance=RequestContext(request))
    else:
        # Dla metody GET - pobierz listę
        if request.method == 'GET':
            ord = Order.objects.all()
            serializer = OrderSerializer(ord, context={'request': request}, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        # Dla metody POST - Utwórz nowego użytkownika
        if request.method == 'POST':
            serializer = OrderSerializer(context={'request': request}, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def order_detail(request, pk):
    if not Login.auth(request):
        msg = u'You are logged out. Please login first.'
        return render_to_response('login.html', { 'msg': msg }, context_instance=RequestContext(request))
    else:
        try:
            ord = Order.objects.get(id=pk)
        except OrderSerializer.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if request.method == 'GET':
            serializer = OrderSerializer(ord, context={'request': request})
            return Response(serializer.data)

        if request.method == 'PUT':
            serializer = OrderSerializer(ord, context={'request': request}, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        if request.method == 'DELETE':
            ord.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

# ArticleUnit
@api_view(['GET', 'POST'])
def articleunits_list(request):
    if not Login.auth(request):
        msg = u'You are logged out. Please login first.'
        return render_to_response('login.html', { 'msg': msg }, context_instance=RequestContext(request))
    else:
        # Dla metody GET - pobierz listę
        if request.method == 'GET':
            au = ArticleUnit.objects.all()
            serializer = ArticleUnitSerializer(au, context={'request': request}, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        # Dla metody POST - Utwórz nowego użytkownika
        if request.method == 'POST':
            serializer = ArticleUnitSerializer(context={'request': request}, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def articleunit_detail(request, pk):
    if not Login.auth(request):
        msg = u'You are logged out. Please login first.'
        return render_to_response('login.html', { 'msg': msg }, context_instance=RequestContext(request))
    else:
        try:
            au = ArticleUnit.objects.get(id=pk)
        except OrderSerializer.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if request.method == 'GET':
            serializer = ArticleUnitSerializer(au, context={'request': request})
            return Response(serializer.data)

        if request.method == 'PUT':
            serializer = ArticleUnitSerializer(au, context={'request': request}, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        if request.method == 'DELETE':
            au.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)