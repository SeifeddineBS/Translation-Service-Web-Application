from django.db import models


class Translation (models.Model) :
    original_text = models.CharField(max_length=1000)
    translated_text = models.CharField(max_length=1000)
    type = models.CharField(max_length=20)
    user = models.CharField(max_length=20)
    # add timestamp

    def __str__ (self):
        return self.translated_text