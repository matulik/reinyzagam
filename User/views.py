#coding=utf-8

# Importowanie metod potrzenych do obsługi widoków
from django.shortcuts import render, render_to_response, RequestContext, redirect
from django.views.decorators.csrf import csrf_exempt

# Importowanie tworzonych przez nas klas
from User.models import User, Login

@csrf_exempt
def login(request):
    # Jeżeli użytkownik jest już zalogowany - przenieś do podstrony
    if Login.auth(request):
        return redirect('/rest/')
    else:
        # Jeżeli zostało wysłane zapytanie
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
                return redirect('/rest/')
            else:
                msg = u'Error. Bad username or password.'
                return render_to_response('login.html', { 'msg': msg }, context_instance=RequestContext(request))

        else:
            return render_to_response('login.html', context_instance=RequestContext(request))

def logout(request):
    if Login.auth(request):
        Login.logout(request)
        msg = u'Logout succesfully.'
        render_to_response('login.html', { 'msg': msg }, context_instance=RequestContext(request))
    else:
        msg = u'You are logged out. Please login first.'
        return render_to_response('login.html', { 'msg': msg }, context_instance=RequestContext(request))