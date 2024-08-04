from django.forms import ValidationError
from django.http import JsonResponse
from .models import Translation
from .serializers import TranslationSerializer

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from bs4 import BeautifulSoup
from rest_framework import serializers




from google.cloud import translate_v2 as translate

def translate_text(text, target_language):
    translate_client = translate.Client()

    result = translate_client.translate(text, target_language=target_language)
    return result['translatedText']



def extract_and_translate(html_content, target_language):
    soup = BeautifulSoup(html_content, 'html.parser')

    # Extract text within <span> tags
    spans = soup.find_all('span')
    translations = {}
    for span in spans:
        if span.string:
            original_text = span.string.strip()
            translated_text = translate_text(original_text, target_language)
            translations[original_text] = translated_text

    # Replace original text with translated text in the soup object
    for span in spans:
        if span.string and span.string.strip() in translations:
            span.string.replace_with(translations[span.string.strip()])

    return str(soup)

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
        type =data.get('type')


    

        if type == Translation.TextType.HTML:
            translated_text = extract_and_translate(original_text,target_language)
        elif type == Translation.TextType.PLAIN_TEXT:
            translated_text = translate_text(original_text,target_language)

        data['translated_text'] = translated_text
        translation = Translation(**data)
        try:
                # Perform model validation
                translation.full_clean()  # This will call the clean method
        except ValidationError as e:
                # If there's a validation error, raise it as a serializer validation error
            raise serializers.ValidationError(e.message_dict)






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
    

    
    