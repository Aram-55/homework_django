import json
from datetime import datetime

from django.views import View
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist

from ..models.Product import Product,TYPE_CHOICES
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
                unit = Unit.objects.get(id=data["unit_id"])
            except ObjectDoesNotExist:
                return JsonResponse({"status": "error", "error": "object unit doesn't exist"}, status=400)
        brand = data.get("brand_id")
        if brand:
            try:
                brand = Brand.objects.get(id=data["brand_id"])
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
        if comment and not isinstance(comment,str):
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
