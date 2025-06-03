# Copyright (C) Takeshi Nakamura. All rights reserved.

from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _
from django_countries.fields import CountryField

from system.models import Attachment

UserModel = get_user_model()


class Wine(models.Model):
    class Status(models.TextChoices):
        LIVE = 'Live', _('active')
        COMBINED = 'Combined', _('Combined')
        DELETED = 'Deleted', _('Deleted')

    class Colour(models.TextChoices):
        RED = 'Red', _('Red')
        WHITE = 'White', _('White')
        ROSE = 'Rose', _('Rose')
        MIXED = 'Mixed', _('Mixed')

    class Type(models.TextChoices):
        WINE = 'Wine', _('Wine')
        BEER = 'Beer', _('Beer')
        CIDER = 'Cider', _('Cider')
        FORTIFIED_WINE = 'Fortified Wine', _('Fortified wine')
        OTHER = 'Other', _('Other')
        SPIRIT = 'Spirit', _('Spirit')
        STILL = 'Still', _('Still')

    class SubType(models.TextChoices):
        ABSINTHE = 'Absinthe', _('Absinthe')
        AQUAVIT = 'Aquavit', _('Aquavit')
        BITTERS = 'Bitters', _('Bitters')
        BRANDY = 'Brandy', _('Brandy')
        CACHACA = 'Cachaca', _('Cachaca')
        GENEVER = 'Genever', _('Genever')
        GIN = 'Gin', _('Gin')
        LIQUEUR = 'Liqueur', _('Liqueur')
        MADEIRA = 'Madeira', _('Madeira')
        MARSALA = 'Marsala', _('Marsala')
        MEZCAL = 'Mezcal', _('Mezcal')
        MONTILLA_MORILES = 'Montilla-Moriles', _('Montilla-Moriles')
        MOSCATEL_DE_SETUBAL = 'Moscatel de Setubal', _('Moscatel de Setubal')
        PORT = 'Port', _('Port')
        RUM = 'Rum', _('Rum')
        RUTHERGLEN = 'Rutherglen', _('Rutherglen')
        SAKE = 'Sake', _('Sake')
        SHERRY = 'Sherry', _('Sherry')
        SHOCHU = 'Shochu', _('Shochu')
        SPARKLING = 'Sparkling', _('Sparkling')
        STILL = 'Still', _('Still')
        TEQUILA = 'Tequila', _('Tequila')
        VERMOUTH = 'Vermouth', _('Vermouth')
        VIN_DOUX_NATUREL = 'Vin Doux Naturel', _('Vin Doux Naturel')
        VODKA = 'Vodka', _('Vodka')
        WHISKIES = 'Whiskies', _('Whiskies')

    lwin = models.BigIntegerField(primary_key=True)
    status = models.CharField(max_length=16, choices=Status)
    display_name = models.CharField(max_length=256)
    producer_title = models.CharField(max_length=64, blank=True)
    producer_name = models.CharField(max_length=128, blank=True)
    wine = models.CharField(max_length=256, blank=True)
    country = CountryField(blank=True)
    region = models.CharField(max_length=64, blank=True)
    sub_region = models.CharField(max_length=64, blank=True)
    site = models.CharField(max_length=64, blank=True)
    parcel = models.CharField(max_length=32, blank=True)
    colour = models.CharField(max_length=16, choices=Colour, blank=True)
    type = models.CharField(max_length=16, choices=Type)
    sub_type = models.CharField(max_length=32, choices=SubType, blank=True)
    designation = models.CharField(max_length=32, blank=True)
    classification = models.CharField(max_length=32, blank=True)
    vintage_config = models.CharField(max_length=20)
    first_vintage = models.IntegerField()
    final_vintage = models.IntegerField()
    date_added = models.DateTimeField()
    date_updated = models.DateTimeField()

    def __str__(self):
        return self.display_name


class Celler(models.Model):
    name = models.CharField(max_length=64, unique=True)
    description = models.TextField(default='', blank=True)

    def __str__(self):
        return self.name


class Bottle(models.Model):
    wine = models.ForeignKey(Wine, on_delete=models.PROTECT)
    vintage = models.IntegerField(default=0)
    description = models.TextField(default='', blank=True)

    images = models.ManyToManyField(Attachment, blank=True)
    celler = models.ForeignKey(
        Celler, on_delete=models.PROTECT, null=True, blank=True,
    )

    acquired = models.DateTimeField()
    price = models.IntegerField(default=0)
    shop = models.CharField(max_length=256, blank=True)

    uncorked = models.DateTimeField(null=True, blank=True)
    score = models.IntegerField(null=True, blank=True)
    comment = models.TextField(default='', blank=True)

    owner = models.ForeignKey(UserModel, on_delete=models.PROTECT)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return f'{self.wine} {self.vintage}'
