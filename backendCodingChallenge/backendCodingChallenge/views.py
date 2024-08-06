from django.forms import ValidationError
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework import status, serializers
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from concurrent.futures import ThreadPoolExecutor
from bs4 import BeautifulSoup
from google.cloud import translate_v2 as translate
from .models import Translation
from .serializers import TranslationSerializer, UserSerializer

# Google Translate API function
def translate_text(text, target_language):
    translate_client = translate.Client()
    result = translate_client.translate(text, target_language=target_language)
    return result['translatedText']



def extract_and_translate(html_content, target_language):
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Collect all text nodes that need to be translated
    text_nodes = [node for node in soup.find_all(string=True) if node.strip()]

    # Define a function to translate and replace text in the node
    def translate_and_replace(text_node):
        original_text = text_node.strip()
        translated_text = translate_text(original_text, target_language)
        text_node.replace_with(translated_text)
    
    # Use ThreadPoolExecutor to parallelize the translation
    with ThreadPoolExecutor() as executor:
        list(executor.map(translate_and_replace, text_nodes))
    
    return str(soup)



# View to handle both listing translations and creating new translations
@api_view(['GET', 'POST'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def translation_list(request):
    """
    GET request: List all translations or filter by the currently authenticated user.
    POST request: Create a new translation with the provided original text and type.
    """
    if request.method == 'GET':
        # Handle GET request to list translations
        user = request.user  # Get the currently authenticated user

        # Check if a specific user ID is provided in query parameters
        if 'user' in request.query_params:
            user_id = request.query_params.get('user')
            if str(user.id) != user_id:  # Ensure the user can only access their own translations
                raise ValidationError('You can only access translations created by yourself.')
            translations = Translation.objects.filter(user=user_id)
        else:
            translations = Translation.objects.all()
        
        # Serialize the translations data and return as JSON response
        serializer = TranslationSerializer(translations, many=True)
        return JsonResponse({"Translations": serializer.data}, safe=False)
    
    elif request.method == 'POST':
        # Handle POST request to create a new translation
        data = request.data.copy() 
        original_text = data.get('original_text') 
        target_language = data.get('target_language')

        # Check if the target language is supported
        SUPPORTED_LANGUAGES = translate.Client().get_languages()
        if not any(item['language'] == target_language for item in SUPPORTED_LANGUAGES):
            return Response({"error": "Unsupported target language."}, status=status.HTTP_400_BAD_REQUEST)

        text_type = data.get('type') 
        
        # Translate the original text based on its type
        if text_type == Translation.TextType.HTML:
            translated_text = extract_and_translate(original_text, target_language)
        elif text_type == Translation.TextType.PLAIN_TEXT:
            translated_text = translate_text(original_text, target_language)
        
        data['translated_text'] = translated_text
        data['user'] = request.user.id
        
        # Create a new Translation instance with the provided data
        translation = Translation(**data)
        try:
            # Perform model validation
            translation.full_clean()  # This calls the clean method to validate data
        except ValidationError as e:
            raise serializers.ValidationError(e.message_dict)
        
        # Serialize the new translation data
        serializer = TranslationSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        # Return validation errors if the serializer is not valid
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)            

# View to handle translation details and deletion
@api_view(['GET','DELETE'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
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
    
# User signup view
@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def signup(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        user = User.objects.get(username=request.data['username'])
        user.set_password(request.data['password'])
        user.save()
        token = Token.objects.create(user=user)
        return Response({'token': token.key, 'user': serializer.data})
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# User login view
@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def login(request):
    user = get_object_or_404(User, username=request.data['username'])
    if not user.check_password(request.data['password']):
        return Response("missing user", status=status.HTTP_404_NOT_FOUND)
    
    token, created = Token.objects.get_or_create(user=user)
    serializer = UserSerializer(user)
    return Response({'token': token.key, 'user': serializer.data})

# Token test view
@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def test_token(request):
    return Response("passed!")

# User logout view
@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def logout(request):
    request.user.auth_token.delete()
    return Response({"User logged out"}, status=status.HTTP_200_OK)