from django.contrib import admin
from django.db import models


class Unit(models.Model):
    code = models.CharField(max_length=36, blank=True, null=True)
    measure = models.CharField(max_length=6)

    def __str__(self):
        return self.code


class UnitAdmin(admin.ModelAdmin):
    list_display = ("id", "code", "measure")
    search_fields = ("id", "code")

    
