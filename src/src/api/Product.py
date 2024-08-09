import json

from django.views import View
from django.http import JsonResponse

from ..models.Product import Product
from ..dry.Product import dry_product
from ..dry.Unit import dry_unit
from ..dry.Brand import dry_brand
class ProductView(View):
    def get(self,request):
        products = Product.objects.all()
        response = [dry_product(product) for product in products]
        return JsonResponse({"data": response,"status": "ok"},status=200)

    def post(self, request):
        data = json.loads(request.body)
        unit = dry_unit(data["unit"])
        brand = dry_brand(data["brand"])
        code = data["code"] if data["code"] else ""
        name = data["name"]
