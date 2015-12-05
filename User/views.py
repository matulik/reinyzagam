#coding=utf-8

# Importowanie metod potrzenych do obsługi widoków
from django.shortcuts import render, render_to_response, RequestContext, redirect
from django.views.decorators.csrf import csrf_exempt

# Importowanie metod potrzebnych do obsługi REST-a
from rest_framework import status
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.decorators import api_view

# Importowanie tworzonych przez nas klas
from User.models import User, Login
from User.serializers import UserSerializer

@csrf_exempt
def login(request):
    # Jeżeli użytkownik jest już zalogowany - przenieś do podstrony
    if Login.auth(request):
        return redirect('/rest/')
    else:
        # Wykonaj, jeżeli zostało wysłane zapytanie
        if request.method == 'POST':
            # Pobieranie danych z zapytania
            username = request.POST['username']
            password = request.POST['password']

            # Sprawdzanie, czy dany użytkownik występuje w bazie
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                msg = u'Error. Bad username or password.'
                return render_to_response('login.html', { 'msg': msg }, context_instance=RequestContext(request))

            # Jeśli użytkownik występuję - sprawdzamy poprawność haseł
            if user.checkPassword(password):
                print u'Login succesfully'
                Login.login(request)
                # Przekierowanie do odpowiedniej podstrony
                return redirect('/rest/')
            else:
                msg = u'Error. Bad username or password.'
                return render_to_response('login.html', { 'msg': msg }, context_instance=RequestContext(request))

        else:
            return render_to_response('login.html', context_instance=RequestContext(request))

@csrf_exempt
def logout(request):
    if Login.auth(request):
        Login.logout(request)
        msg = u'Logout succesfully.'
        return render_to_response('login.html', { 'msg': msg }, context_instance=RequestContext(request))
    else:
        msg = u'You are logged out. Please login first.'
        return render_to_response('login.html', { 'msg': msg }, context_instance=RequestContext(request))

@api_view(['GET'])
def api_root(request):
    '''
    Metoda służąca do zwrócenia listy widoków API
    W przyszłości może przydać się do utworzenia "Drzewa" danych
    '''
    return Response({
        'users_list': reverse('users_list', request=request),
        'locations_list': reverse('locations_list', request=request),
        'buyers_list': reverse('buyers_list', request=request),
        'categories_list': reverse('categories_list', request=request),
        'articles_list': reverse('articles_list', request=request),
        'orders_list': reverse('orders_list', request=request),

    })

@api_view(['GET', 'POST'])
def users_list(request):
    '''
    Widok dla listy użytkowników (w tym dodawanie użytkownika); url: /rest/users_list/
    '''
    if not Login.auth(request):
        msg = u'You are logged out. Please login first.'
        return render_to_response('login.html', { 'msg': msg }, context_instance=RequestContext(request))
    else:
        # Dla metody GET - pobierz listę
        if request.method == 'GET':
            users = User.objects.all()
            serializer = UserSerializer(users, context={'request': request}, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        # Dla metody POST - Utwórz nowego użytkownika
        if request.method == 'POST':
            serializer = UserSerializer(context={'request': request}, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def user_detail(request, pk):
    '''
    Widok dla detali użytkownika (pokaż, aktualizuj, usuń); url: /rest/user_detail/
    Argument pk funkcji to parametr id URLa (GET)
    '''
    if not Login.auth(request):
        msg = u'You are logged out. Please login first.'
        return render_to_response('login.html', { 'msg': msg }, context_instance=RequestContext(request))
    else:
        # Sprawdzamy czy dany użytkownik istnieje w bazie
        try:
            user = User.objects.get(id=pk)
        except User.DoesNotExist:
            # Jeślni nie, zwracamy status code NOT FOUND
            return Response(status=status.HTTP_404_NOT_FOUND)

        # Pobierz użytkownika
        if request.method == 'GET':
            serializer = UserSerializer(user, context={'request': request})
            return Response(serializer.data)

        # Edytuj użytkownika
        if request.method == 'PUT':
            # Zapisujemy zmiany. request.data - dane podane w zapytaniu, partial - umożliwia "nadpisanie" danych
            serializer = UserSerializer(user, context={'request': request}, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            else:
                # Jeżeli wystąpił błąd, zwracamy BAD REQUEST
                # UWAGA! Jeżeli zostały wprowadzone złe dane należy posłużyć się wtyczką do przeglądarki
                # np. Firebug. W tym miejscu nie są zwracane informacje na temat złych danych!
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Usuń użytkownika
        if request.method == 'DELETE':
            user.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
