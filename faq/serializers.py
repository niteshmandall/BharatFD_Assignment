from rest_framework import serializers
from .models import FAQ


class FAQSerializer(serializers.ModelSerializer):
    # answer_en = serializers.CharField()  # Explicitly define the field

    class Meta:
        model = FAQ
        fields = ["question_en", "answer_en", "question_hi", "question_bn"]
