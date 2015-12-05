# coding=UTF-8

from django.db import models
from django.utils import timezone
from decimal import Decimal

# Exceptions
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned

# User
from User.models import User, Login


class Category(models.Model):
    """
    Opisuje katagorię produktów
    """
    name = models.CharField(max_length=500, blank=False, verbose_name=u'Kategoria')
    description = models.CharField(max_length=1000, verbose_name=u'Opis kategorii')

    @staticmethod
    def add_category(name, description):
        """
        Dodaje nową kategorię. Statyczna, aby uniknąć tworzenia nowej instancji klasy
        :param name: nazwa kategorii
        :param description: opis kategorii
        :return: brak
        """
        cat = Category()
        cat.name = name
        cat.description = description
        cat.save()

    def change_category(self, name, description):
        """
        Zmienia dane aktualnej kategorii
        :param name: nazwa kategorii
        :param description: opis kategorii
        :return:
        """
        if name:
            self.name = name
        if description:
            self.description = description

    def delete_category(self):
        """
        Usuwa aktualną kategorię
        :return: brak
        """
        self.delete()

    @staticmethod
    def delete_category_by_id(id):
        """
        Usuwa kategorię przez jej id
        :param id: id kategorii
        :return: True jesli poprawno usunięto kategorię, False jeśli wystąpił wyjątek
        """
        try:
            Category.objects.get(id=int(id)).delete()
            return True
        except ObjectDoesNotExist:
            return False
        except MultipleObjectsReturned:
            return False


class Article(models.Model):
    """
    Opisuje artykuł (ogólnie, nie jednostkowo)
    """
    name = models.CharField(max_length=500, blank=False, verbose_name=u'Nazwa przedmiotu')
    category = models.ForeignKey(Category)
    quantity = models.IntegerField(default=0, verbose_name=u'Aktualny stan magazynowy')
    cost = models.DecimalField(decimal_places=2, max_digits=6, verbose_name=u'Cena jednostkowa')
    dateAdded = models.DateTimeField(default=timezone.now)
    whoAdded = models.ForeignKey(User)

    @staticmethod
    def add_article(name, categoryID, cost, request):
        """
        Dodaje nowy artykuł. Metoda statyczna, by uniknąć tworzenia nowej instancji klasy.
        :param name: nazwa artykułu
        :param categoryID: id kategorii
        :param cost: cena artykułu
        :param request: dane aktualnej sesji
        :return:
        """
        article = Article()
        article.name = str(name)
        article.category = Category.objects.get(id=categoryID)
        article.cost = Decimal(float(cost))
        article.whoAdded = Login.get_current_user(request)
        article.save()
        return article

    @staticmethod
    def exist(name):
        """
        Metoda sprawdza, czy dany artukuł istnieje
        :param name: nazwa artukułu
        :return: True jeśli istnieje, false jeśli nie istnieje
        """
        try:
            Article.objects.get(name=name)
        except ObjectDoesNotExist:
            return False
        except MultipleObjectsReturned:
            return True

    def decreasQuantity(self):
        self.quantity = self.quantity - 1

    def increaseQuanity(self):
        self.quantity = self.quantity + 1

    def change_article(self, name, category, quantity, cost):
        """
        Zmienia informacje dotyczące artykułu
        :param name: nazwa artykułu
        :param category: kategoria artykułu
        :param quantity: ilość danego artukułu
        :param cost: cena artukułu
        :return:
        """
        if name:
            self.name = name
        if category:
            self.category = category
        if quantity:
            self.quantity = quantity
        if cost:
            self.cost = cost

    def delete_article(self):
        """
        Usuwa aktualny artykuł
        :return: brak
        """
        self.delete()

    @staticmethod
    def delete_article_by_id(id):
        """
        Usuwa artukuł poprzez jego id
        :param id: id artukułu
        :return: True jeśli usunięto, false jeśli wystąpił wyjątek
        """
        try:
            Article.objects.get(id=int(id)).delete()
            return True
        except ObjectDoesNotExist:
            return False
        except MultipleObjectsReturned:
            return False


class Buyer(models.Model):
    """
    Klasa opisująca kupującego
    """
    name = models.CharField(max_length=100, blank=False, verbose_name=u'Nazwa kupującego')
    firstName = models.CharField(max_length=50, verbose_name=u'Imię')
    surname = models.CharField(max_length=50, verbose_name=u'Nazwisko')
    NIP = models.CharField(max_length=13, verbose_name=u'NIP')
    address = models.TextField(verbose_name=u'Adres')

    @staticmethod
    def add_buyer(name, firstName, surname, NIP, address):
        """
        Klasa dodaje nowego kupującego. Metoda statyczna, by uniknąc tworzenia nowej instancji klasy
        :param name: nazwa kupującego
        :param firstName: imię kupującego
        :param surname: nazwisko kupującego
        :param NIP: NIP kupującego
        :param address: adres kupującego
        :return: brak
        """
        buyer = Buyer()
        buyer.name = name
        buyer.firstName = firstName
        buyer.surname = surname
        buyer.NIP = NIP
        buyer.address = address
        buyer.save()

    def change_buyer(self, name, firstName, surname, NIP, address):
        """
        Zmienia informacje odnośnie kupującego
        :param name: nazwa kupującego
        :param firstName: imię kupującego
        :param surname: nazwisko kupującego
        :param NIP: NIP kupującego
        :param address: adres kupującego
        :return: brak
        """
        if name:
            self.name = name
        if firstName:
            self.firstName = firstName
        if surname:
            self.surname = surname
        if NIP:
            self.NIP = NIP
        if address:
            self.address = address

    def delete_buyer(self):
        """
        Usuwa aktualnego kupującego
        :return: brak
        """
        self.delete()

    @staticmethod
    def delete_buyer_by_id(id):
        """
        Usuwa kupującego poprzez jego id
        :param id: id kupującego
        :return: True jeśli poprawno usunięto kupującego, False jeśli wystąpił wyjątek
        """
        try:
            Buyer.objects.get(id=int(id)).delete()
            return True
        except ObjectDoesNotExist:
            return False
        except MultipleObjectsReturned:
            return False


class Order(models.Model):
    """
    Klasa opisująca zamówienie
    """
    cost = models.DecimalField(decimal_places=2, max_digits=6, default=0.00, verbose_name=u'Ogólny koszt')
    discount = models.DecimalField(decimal_places=2, max_digits=6, default=0.00)
    dateOrder = models.DateTimeField(default=timezone.now)
    dateSpend = models.DateTimeField(default=None, null=True)
    released = models.BooleanField(default=False)
    buyer = models.ForeignKey(Buyer, verbose_name=u'Klient')
    whoAdded = models.ForeignKey(User, related_name='whoAdded')
    whoReleased = models.ForeignKey(User, related_name='whoReleased', null=True)

    @staticmethod
    def add_order(buyer, request):
        """
        Metoda dodająca zamówienie
        :param buyer: kupujący
        :param request: dane sesji
        :return: zwraca id nowo utworzonego zamówienia
        """
        order = Order()
        order.buyer = buyer
        order.whoAdded = Login.get_current_user(request)
        order.save()
        return order

    def recount_order(self):
        """
        Metoda przelicza nową wartość zamówienia
        :return: brak - nowa wartość przechowywana jest w prametrze cost
        """
        articles = ArticleUnit.objects.filter(order=self)
        print len(articles)
        article_sum = Decimal('0')
        for a in articles:
            article = Article.objects.get(id=a.articleID_id)
            article_sum = article_sum + article.cost
        self.cost = article_sum
        self.save()

    def set_released(self, request):
        """
        Ustawia zamówienia jako wydane
        :param request: dane sesji
        :return: brak
        """
        self.released = True
        self.dateSpend = timezone.now()
        self.whoReleased = Login.get_current_user(request)
        self.save()

    def set_unreleased(self):
        """
        Ustawia zamówienie jako niewydane (np zwrot)
        :return: brak
        """
        self.whoReleased = None
        self.released = False
        self.save()

    def change_order(self, discount, dateOrder, dateSpend, released, buyer):
        """
        Zmienia dane zamówienia
        :param discount: upust
        :param dateOrder: data zamówienia
        :param dateSpend: data wydania
        :param released: czy wydane
        :param buyer: kupujący
        :return:
        """
        if discount:
            self.discount = discount
        if dateOrder:
            self.dateOrder = dateOrder
        if dateSpend:
            self.dateSpend = dateSpend
        if released:
            self.released = released
        if buyer:
            self.buyer = buyer

    def delete_order(self):
        """
        Usuwa aktualne zamowienie
        :return:
        """
        self.delete()


class Location(models.Model):
    """
    Opisuje lokacje (miejsce) przechowywania artykułu
    """
    name = models.CharField(max_length=100, blank=False, verbose_name=u'Nazwa lokalizacji')
    description = models.CharField(max_length=1000, verbose_name=u'Opis')

    @staticmethod
    def add_location(name, description):
        """
        Dodaje nową lokację. Metoda statyczna, by uniknąć tworzenia nowej instancji klasy
        :param name: nazwa lokacji
        :param description: opis lokacji
        :return: brak
        """
        location = Location()
        location.name = name
        location.description = description
        location.save()

    def change_location(self, name, description):
        """
        Zmienia informacje na temat lokacji
        :param name: nazwa lokacji
        :param description: opis lokacji
        :return: brak
        """
        if name:
            self.name = name
        if description:
            self.description = description

    def delete_location(self):
        """
        Usuwa aktualną lokacje
        :return: brak
        """
        self.delete()

    @staticmethod
    def delete_location_by_id(id):
        """
        Usuwa lokacje porpzez jej id
        :param id: id lokacji
        :return: True jeśli poprawnie usunięto, False jeśli wystąpił wyjątek
        """
        try:
            Location.objects.get(id=int(id)).delete()
            return True
        except ObjectDoesNotExist:
            return False
        except MultipleObjectsReturned:
            return False


class ArticleUnit(models.Model):
    """
    Klasa opisująca jednostkę artykułu.
    Określa jaki artukuł, gdzie występuję oraz do jakiego zamówienia jest przypisany.
    """
    location = models.ForeignKey(Location, verbose_name=u'Lokalizacja')
    article = models.ForeignKey(Article, verbose_name=u'Artykuł')
    order = models.ForeignKey(Order, verbose_name=u'Zamówienie', null=True)
    dateInserted = models.DateTimeField(default=timezone.now)
    available = models.BooleanField(default=True)
    whoAdded = models.ForeignKey(User)

    @staticmethod
    def add_articleunit(location, article, order, dateInserted, request):
        """
        Dodaje nową jednostkę
        :param location: lokacja jednostki
        :param article: artykuł ogólny
        :param order: przypisane zamówienie
        :param dateInserted: data dodania do bazy
        :param request: dane sesji
        :return: brak
        """
        articleunit = ArticleUnit()
        articleunit.location = location
        # Zwiększenie dostępności o jeden
        article.increaseQuanity()
        articleunit.article = article
        articleunit.order = order
        if dateInserted:
            articleunit.dateInserted = dateInserted
        else:
            articleunit.dateInserted = timezone.now
        articleunit.whoAdded = Login.get_current_user(request)
        articleunit.save()

    def set_to_order(self, orderID):
        """
        Przypisuje do zamówienia o podanym id
        :param orderID: id zamówienia
        :return: brak
        """
        self.orderID = Order.objects.get(id=orderID)
        self.available = False
        order = Order.objects.get(id=int(orderID))
        order.recount_order()
        self.save()

    def change_articleunit(self, location, article, order, dateInserted):
        """
        Zmienia informacje o jednostce
        :param location: lokacja jednostki
        :param article: artykuł ogólny
        :param order: przypisane zamówienie
        :param dateInserted: data dodania do bazy
        :return:
        """
        if location:
            self.location = location
        if article:
            self.article = article
        if orderID:
            self.order = order
        if dateInserted:
            self.dateInserted = dateInserted

    def delete_articleunit(self):
        """
        Usuwa aktualny artykuł
        :return: brak
        """
        self.article.decreasQuantity()
        self.delete()

    def set_available(self):
        """
        Ustawia stan artykułu na dostępny
        :return: brak
        """
        if self.available == False:
            self.article.increaseQuanity()
        self.available = True

    def set_unavailable(self):
        """
        Ustawia stan artykułu na niedostępny
        :return: brak
        """
        if self.available == True:
            self.article.decreasQuantity()
        self.available = False
