from django.contrib import admin
from .models import FAQ
from ckeditor.widgets import CKEditorWidget
from django import forms


class FAQForm(forms.ModelForm):
    class Meta:
        model = FAQ
        fields = "__all__"
        widgets = {
            "answer_en": CKEditorWidget(),  # WYSIWYG editor for answers
        }


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    form = FAQForm
    list_display = ("question_en", "question_hi", "question_bn")  # Show translations
