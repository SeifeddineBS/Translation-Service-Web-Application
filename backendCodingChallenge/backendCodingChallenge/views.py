from django.http import JsonResponse
from .models import Translation
from .serializers import TranslationSerializer

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status


from google.cloud import translate_v2 as translate

def translate_text(text, target_language):
    translate_client = translate.Client()

    result = translate_client.translate(text, target_language=target_language)
    return result['translatedText']

@api_view(['GET','POST'])
def translation_list(request):
    if request.method == 'GET':
        # get all translations 
        translations =Translation.objects.all()
        serializer =TranslationSerializer(translations,many=True)
        return JsonResponse({"Translations" :serializer.data}, safe=False)
    elif request.method == 'POST':
        data = request.data.copy()
        original_text = data.get('original_text')
        target_language = 'de'

        # Perform the translation
        translated_text = translate_text(original_text, target_language)
        data['translated_text'] = translated_text

        serializer = TranslationSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
@api_view(['GET','DELETE'])
def translation_details(request,id):
    try:
        translation = Translation.objects.get(pk=id)
    except Translation.DoesNotExist:
        return Response(status = status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = TranslationSerializer(translation)
        return Response(serializer.data)
    elif request.method == 'DELETE':
        translation.delete()
        return Response(status = status.HTTP_204_NO_CONTENT)
    

    
    