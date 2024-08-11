import json
import datetime

from django.views import View
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist

from ..models.Product import Product, TYPE_CHOICES
from ..models.Unit import Unit
from ..models.Brand import Brand
from ..dry.Product import dry_product


class ProductView(View):
    def get(self, request):
        products = Product.objects.all()
        response = [dry_product(product) for product in products]
        return JsonResponse({"data": response, "status": "ok"}, status=200)

    def post(self, request):
        data = json.loads(request.body)
        unit = data.get("unit_id")
        if unit:
            try:
                unit = Unit.objects.get(id=unit)
            except ObjectDoesNotExist:
                return JsonResponse({"status": "error", "error": "object unit doesn't exist"}, status=400)
        brand = data.get("brand_id")
        if brand:
            try:
                brand = Brand.objects.get(id=brand)
            except ObjectDoesNotExist:
                return JsonResponse({"status": "error", "error": "object brand doesn't exist"}, status=400)
        code = data.get("code")
        if code and not isinstance(code, str):
            return JsonResponse({"status": "error", "error": "code must be string"}, status=400)
        name = data.get("name")
        if name and not isinstance(name, str):
            return JsonResponse({"status": "error", "error": "name must be string"}, status=400)
        elif not name:
            return JsonResponse({"status": "error", "error": "name is required"}, status=400)
        weight = data.get("weight")
        if weight and not isinstance(weight, float):
            return JsonResponse({"status": "error", "error": "weight must be float"}, status=400)
        buy_date = data.get("buy_date")
        # if buy_date and not isinstance(buy_date,datetime):
        #     return JsonResponse({"status": "error", "error": "buy_date must be datetime"}, status=400)
        type = data.get("type")
        if type and not TYPE_CHOICES.get(type):
            return JsonResponse({"status": "error", "error": "type must be one of TYPE_CHOICES"}, status=400)
        comment = data.get("comment")
        if comment and not isinstance(comment, str):
            return JsonResponse({"status": "error", "error": "comment must be string"}, status=400)
        product = Product.objects.create(
            unit=unit,
            brand=brand,
            code=code,
            name=name,
            weight=weight,
            buy_date=buy_date,
            type=type,
            comment=comment
        )
        return JsonResponse({"data": dry_product(product), "status": "ok"}, status=200)

    def patch(self, request):
        product_id = request.GET.get("id")
        if isinstance(product_id, int):
            product = Product.objects.get(pk=product_id)
        else:
            return JsonResponse({"status": "error", "error": "id must be integer"}, status=400)
        data = json.loads(request.body)
        if "unit_id" in data and isinstance(data["unit_id"], int):
            try:
                unit = Unit.objects.get(id=data["unit_id"])
                product.unit = unit
            except ObjectDoesNotExist:
                return JsonResponse({"status": "error", "error": "object unit doesn't exist"}, status=400)
        if "brand_id" in data and isinstance(data["brand_id"], int):
            try:
                brand = Brand.objects.get(id=data["brand_id"])
                product.brand = brand
            except ObjectDoesNotExist:
                return JsonResponse({"status": "error", "error": "object brand doesn't exist"}, status=400)
        if "code" in data and isinstance(data["code"], str):
            product.code = data["code"]
        if "name" in data and isinstance(data["name"], str):
            product.name = data["name"]
        if "weight" in data and isinstance(data["weight"], float):
            product.weight = data["weight"]
        if "buy_date" in data and isinstance(data["but_date"], datetime.date):
            product.buy_date = data["buy_date"]
        if "type" in data and data["type"] in TYPE_CHOICES and isinstance(data["type"], int):
            product.type = data["type"]
        if "comment" in data and isinstance("comment", str):
            product.comment = data["comment"]
        product.save()
        return JsonResponse({"data": dry_product(product)}, status=200)

    def delete(self, request):
        product_id = request.GET.get("id")
        try:
            product = Product.objects.get(id=product_id)
        except ObjectDoesNotExist:
            return JsonResponse({"status": "error", "error": "object product doesn't exist"}, status=400)
        product.delete()
        return JsonResponse({"status": "ok"}, status=200)
