from django.db import models
from django.contrib import admin
from .Unit import Unit
from .Brand import Brand

TYPE_CHOICES = ("Ապրանք", "Ծառայություն", "Պրոյեկտ", "Արտադրանք")


class Product(models.Model):
    unit = models.ForeignKey(Unit, on_delete=models.SET_NULL, blank=True, null=True)
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, blank=True, null=True)
    code = models.CharField(max_length=36, blank=True, null=True)
    name = models.CharField(max_length=255)
    weight = models.FloatField(blank=True, null=True)
    buy_date = models.DateField(blank=True, null=True)
    type = models.CharField(choices=TYPE_CHOICES)
    comment = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "unit_info", "brand_info", "code", "name", "weight", "buy_date", "type", "comment")
    search_fields = ("id", "name", "code")
