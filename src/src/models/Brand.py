from django.db import models
from django.contrib import admin


class Brand(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class BrandAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("id", "name")
