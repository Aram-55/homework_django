import json

from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.views import View

from ..models.Unit import Unit
from ..dry.Unit import dry_unit


class UnitView(View):
    def get(self, request):
        units = Unit.objects.all()
        response = [dry_unit(unit) for unit in units]
        return JsonResponse({"data": response}, status=200)

    def post(self, request):
        data = json.loads(request.body)
        code = data.get("code")
        if code and not isinstance(data["code"], str):
            return JsonResponse({"status": "error", "error": "code must be string"}, status=400)
        if "measure" in data and isinstance(data["measure"], str):
            measure = data["measure"]
        else:
            return JsonResponse({"status": "error", "error": "measure must be string"}, status=400)
        unit = Unit.objects.create(
            code=code,
            measure=measure
        )
        return JsonResponse({"data": unit}, status=200)

    def patch(self, request):
        unit_id = request.GET.get("id")
        try:
            unit = Unit.objects.get(id=unit_id)
        except ObjectDoesNotExist:
            return JsonResponse({"status": "Error", "error": "unit object doesn't exist"}, status=400)
        data = json.loads(request.body)
        unit.code = data.get("code")
        if code and not isinstance(data["code"], str):
            return JsonResponse({"status": "error", "error": "code must be string"}, status=400)
        if "measure" in data:
            if isinstance(data["measure"], str):
                unit.measure = data["measure"]
            else:
                return JsonResponse({"status": "error", "error": "measure must be string"}, status=400)
        unit.save()
        return JsonResponse({"data": unit}, status=200)

    def delete(self, request):
        unit_id = request.GET.get("id")
        try:
            unit = Unit.objects.get(id=unit_id)
        except ObjectDoesNotExist:
            return JsonResponse({"status": "Error", "error": "unit object doesn't exist"}, status=400)
        unit.delete()
        return JsonResponse({"status": "ok"}, status=200)
