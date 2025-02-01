from django.db import models
from ckeditor.fields import RichTextField
from googletrans import Translator


class FAQ(models.Model):
    question_en = models.TextField()
    answer_en = RichTextField()
    question_hi = models.TextField(blank=True, null=True)
    question_bn = models.TextField(blank=True, null=True)
    # Add more language fields as needed

    def get_translated_question(self, lang):
        """Return translated question or fallback to English."""
        return getattr(self, f"question_{lang}", None) or self.question_en

    def save(self, *args, **kwargs):
        translator = Translator()
        # Always update translations from the current English value
        self.question_hi = translator.translate(self.question_en, dest="hi").text
        self.question_bn = translator.translate(self.question_en, dest="bn").text
        super().save(*args, **kwargs)
