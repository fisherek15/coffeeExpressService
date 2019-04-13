from multiselectfield import MultiSelectField
from django.core.validators import RegexValidator
from django.db import models
from datetime import datetime
from django.core.validators import MinValueValidator
from decimal import *
from django.conf import settings


class Device(models.Model):
    producer = models.CharField(max_length=50, verbose_name="Producent")
    model = models.CharField(max_length=50, verbose_name="Model")
    id_number = models.CharField(max_length=50, null=True, blank=True, verbose_name="Numer seryjny")

    def __str__(self):
        return self.producer + " " + self.type + " " + self.model + " " + self.id_number


class Customer(models.Model):
    first_name = models.CharField(max_length=30, verbose_name="Imię")
    last_name = models.CharField(max_length=60, verbose_name="Nazwisko")
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Numer telefonu musi się składać z 9-15 znaków i może być poprzedzony znakiem '+'. ")
    phone_number = models.CharField(validators=[phone_regex], max_length=17, verbose_name="Telefon")
    email = models.EmailField(max_length=64, null=True, blank=True, verbose_name="Email")

    def __str__(self):
        return self.first_name


class Order(models.Model):
    order_id = models.CharField(unique=True, max_length=20, verbose_name="Numer zgłoszenia", error_messages={'unique':"Wprowadzony numer zgłoszenia już istnieje!"})
    order_type = models.CharField(max_length=60, verbose_name="Rodzaj zlecenia")
    acceptance_date = models.DateField(default=datetime.now, verbose_name="Data przyjęcia zgłoszenia")
    description_for_service = models.TextField(verbose_name="Opis dla serwisu")
    description_from_service = models.TextField(null=True, blank=True, verbose_name="Opis od serwisu")
    description_for_customer = models.TextField(null=True, blank=True, verbose_name="Opis dla klienta")

    ACTIVITIES = (('Odkawianie', 'Odkawianie'),
                  ('Odkamienianie', 'Odkamienianie'),
                  ('Czyszczenie bloku', 'Czyszczenie bloku'),
                  ('Wymiana uszczelek', 'Wymiana uszczelek'))
    realized_activity = MultiSelectField(choices=ACTIVITIES, null=True, blank=True, verbose_name="Wykonana czynność")
    max_repair_cost = models.DecimalField(
        max_digits=7,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))],
        default=300,
        verbose_name="Maksymalny koszt naprawy bez konsultacji z serwisem")
    technical_condition = models.TextField(verbose_name="Stan techniczny / brakujące elementy")
    service_repair_cost = models.DecimalField(
        max_digits=7,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(Decimal('0.00'))],
        verbose_name="Koszty poniesione przez serwis")
    sms_sent_date = models.DateField(null=True, blank=True, verbose_name="Data wysłania SMSa z powiadomieniem do klienta")
    repair_cost = models.DecimalField(
        max_digits=7,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(Decimal('0.00'))],
        verbose_name="Całkowity koszt usługi")
    return_date = models.DateField(null=True, blank=True, verbose_name="Data odebrania urządzenia przez klienta")
    device = models.OneToOneField(Device, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)

    def __str__(self):
        return self.full_data()

    def full_data(self):
        return self.order_id + " " + str(self.acceptance_date)


class Comment(models.Model):
    content = models.TextField(verbose_name="Twój komentarz")
    published_date = models.DateTimeField(default=datetime.now)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)


class Status(models.Model):
    content = models.TextField(verbose_name="Status zgłoszenia")
    date_of_change = models.DateTimeField(default=datetime.now)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

