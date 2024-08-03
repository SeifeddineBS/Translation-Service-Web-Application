from django.http import JsonResponse
from .models import Translation
from .serializers import TranslationSerializer

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

@api_view(['GET','POST'])
def translation_list(request):
    if request.method == 'GET':
        # get all translations 
        translations =Translation.objects.all()
        serializer =TranslationSerializer(translations,many=True)
        return JsonResponse({"Translations" :serializer.data}, safe=False)
    elif request.method == 'POST':
        serializer = TranslationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data , status= status.HTTP_201_CREATED)