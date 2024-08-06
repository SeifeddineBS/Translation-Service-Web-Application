from django.db import models
from django.core.exceptions import ValidationError
import re


class Translation (models.Model) :

    class TextType(models.TextChoices):
        HTML = 'HTML', 'HTML'
        PLAIN_TEXT = 'PLAIN_TEXT', 'PLAIN_TEXT'

    type = models.CharField(
        #Text type choices
        max_length=10,
        choices=TextType.choices,
        default=TextType.PLAIN_TEXT
    )

    original_text = models.CharField(max_length=1000)
    translated_text = models.CharField(max_length=1000)
    user = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__ (self):
        return self.translated_text
    
    def clean(self):
        #Validate text type
        super().clean()

        if self.type == Translation.TextType.HTML:
            if not self.is_html(self.original_text):
                raise ValidationError('When type is HTML, the original text must be valid HTML content.')

        elif self.type == Translation.TextType.PLAIN_TEXT:
            if self.is_html(self.original_text):
                raise ValidationError('When type is Plain Text, the original text must not contain HTML.')

    def is_html(self, text):
        #Check for HTML tags
        html_tag_pattern = re.compile(r'<[^>]+>')
        return bool(html_tag_pattern.search(text))