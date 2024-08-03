from django.http import JsonResponse
from .models import Translation
from .serializers import serializer

def translation_list(request) :
    # get all translations 
    translations =Translation.objects.all()
    serializer(translations,many=True)
    return JsonResponse(serializer.data)