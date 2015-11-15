#coding=UTF-8

from django.db import models
from hashlib import sha1

# Create your models here.

class User(models.Model):
    username = models.CharField(max_length=50, blank=False, verbose_name=u'Login')
    password = models.CharField(max_length=50, blank=False, verbose_name=u'Hasło')
    firstname = models.CharField(max_length=50, verbose_name=u'Imię')
    surname = models.CharField(max_length=50, verbose_name=u'Nazwisko')
    email = models.EmailField()
    access_lvl = models.IntegerField(default=0, verbose_name=u'Poziom dostępu')

    def hashPassword(self, password):
        """
        Metoda szyfrująca hasło
        :param password: Aktualne hasło
        :return: Zaszyfrowane hasło poprzez SHA1
        """
        return sha1(password.encode('utf8')).hexdigest()

    def checkPassword(self, password):
        """
        Metoda sprawdzająca podane hasło z aktualnym
        :param password: hasło do sprawdzenia
        :return: True jeśli hasłą są zgodne, False jeśli nie zgodne
        """
        if sha1(password.encode('utf8')).hexdigest() == self.password:
            return True
        else:
            return False


    def changePassword(self, oldPassword, newPassword):
        """
        Metoda porównóje stare hasło z aktualnym i jeśli jest poprawne, zamienia je
        :param oldPassword: stare hasło
        :param newPassword: nowe hasło
        :return: True jeśli operacja się powiedzie
        """
        if self.checkPassword(oldPassword):
            self.password = self.hashPassword(newPassword)
            self.save()
            return True
        else:
            print u'Podane hasło nie jest zgodne z istniejącym.'
            return False

class Login():
    @staticmethod
    def login(request):
        """
        Metoda loguje użytkownika w sesji, dzięki parametrom przekazanym przez POST
        :param request: parameter request podawany z widoku zawierający dane o sesji
        :return: True jeśli zalogowano poprawnie, False jeśli nie (złe dane)
        """
        username = request.POST['username']
        password = request.POST['password']
        try:
            user = User.objects.get(username=username)
        except ObjectDoesNotExist:
            print u'Podany zły login lub hasło.'
            return False
        if user and user.checkPassword(password):
            request.session['login'] = True
            request.session['id'] = user.id
            print u'Poprawnie zalogowano.'
            return True
        else:
            print u'Podany zły login lub hasło.'
            return False

    @staticmethod
    def logout(request):
        """
        Metoda wylogowuje użytkownika z sesji oraz czyści ją
        :param request: parameter request podawany z widoku zawierający dane o sesji
        :return: brak
        """
        request.session.flush()
        request.session['login'] = False
        request.session['id'] = None
        print u'Wylogowano.'

    @staticmethod
    def auth(request):
        """
        Metoda sprawdza, czy użytkownik jest zalogowany
        :param request: parameter request podawany z widoku zawierający dane o sesji
        :return: True jeśli zalogowany, False jeśli nie
        """
        if not request.session.get('login', None) or not request.session.get('id', None):
            return False
        if request.session['login'] == True and request.session['id'] != None:
            return True
        else:
            return False

    @staticmethod
    def get_current_user(request):
        """
        Metoda pobiera informacje o aktualnym użytkowniku na podstawie jego id i zwraca jako obiekt User
        :param request: parameter request podawany z widoku zawierający dane o sesji
        :return: zwraca użytkownika o danym id
        """
        user = User.objects.get(id=request.session['id'])
        return user
