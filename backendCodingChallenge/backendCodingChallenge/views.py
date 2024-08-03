from django.http import JsonResponse
from .models import Translation
from .serializers import TranslationSerializer

def translation_list(request):
    # get all translations 
    translations =Translation.objects.all()
    serializer =TranslationSerializer(translations,many=True)
    return JsonResponse({"Translations" :serializer.data}, safe=False)