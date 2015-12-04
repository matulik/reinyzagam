#coding=utf8

from django.shortcuts import render

from django.shortcuts import render, render_to_response, RequestContext, redirect

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from User.models import Login

from Store.models import Location
from Store.serializers import LocationSerializer

@api_view(['GET', 'POST'])
def locations_list(request):
    if not Login.auth(request):
        msg = u'You are logged out. Please login first.'
        return render_to_response('login.html', { 'msg': msg }, context_instance=RequestContext(request))
    else:
        # Dla metody GET - pobierz listę
        if request.method == 'GET':
            users = Location.objects.all()
            serializer = LocationSerializer(users, context={'request': request}, many=True)
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
            user = Location.objects.get(id=pk)
        except Location.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if request.method == 'GET':
            serializer = LocationSerializer(user, context={'request': request})
            return Response(serializer.data)

        if request.method == 'PUT':
            serializer = LocationSerializer(user, context={'request': request}, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        if request.method == 'DELETE':
            user.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
