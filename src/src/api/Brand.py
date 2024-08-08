import json

from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.views import View
from ..models.Brand import Brand
from ..dry.Brand import dry_brand


class BrandView(View):
    def get(self, request):
        brands = Brand.objects.all()
        response = {"data": [dry_brand(brand) for brand in brands]}
        return JsonResponse(response, status=200)

    def post(self, request):
        data = json.loads(request.body)
        if isinstance(data["name"], str):
            name = data["name"]
        else:
            return JsonResponse({"status": "Error", "error": "name must be string"}, status=400)
        brand = Brand.objects.create(
            name=name
        )
        return JsonResponse({"status": "ok", "id": brand.id}, status=200)

    def patch(self, request):
        brand_id = request.GET.get("id")
        data = json.loads(request.body)
        try:
            brand = Brand.objects.get(id=brand_id)
        except ObjectDoesNotExist:
            return JsonResponse({"status": "Error", "error": "brand object doesn't exist"}, status=400)
        if "name" in data:
            brand.name = data["name"]
        brand.save()
        return JsonResponse({"status": "ok", "id": brand.id}, status=200)

    def delete(self, request):
        brand_id = request.GET.get("id")
        try:
            brand = Brand.objects.get(id=brand_id)
        except ObjectDoesNotExist:
            return JsonResponse({"status": "Error", "error": "brand object doesn't exist"}, status=400)
        brand.delete()
        return JsonResponse({"status": "ok"}, status=200)
