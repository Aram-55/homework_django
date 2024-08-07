from django.contrib import admin
from .Brand import Brand, BrandAdmin
from .Product import Product, ProductAdmin
from .Unit import Unit, UnitAdmin

admin.site.register(Brand, BrandAdmin)
admin.site.register(Unit, UnitAdmin)
admin.site.register(Product, ProductAdmin)
