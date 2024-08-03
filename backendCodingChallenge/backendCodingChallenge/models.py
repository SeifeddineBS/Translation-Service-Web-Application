from django.db import models


class Translation (models.Model) :

    class TextType(models.TextChoices):
        HTML = 'HTML', 'HTML'
        PLAIN_TEXT = 'PLAIN_TEXT', 'PLAIN_TEXT'

    type = models.CharField(
        max_length=10,
        choices=TextType.choices,
        default=TextType.PLAIN_TEXT
    )

    original_text = models.CharField(max_length=1000)
    translated_text = models.CharField(max_length=1000)
    user = models.CharField(max_length=20)
    # add timestamp

    def __str__ (self):
        return self.translated_text