from rest_framework import serializers
from main.models import QuizQuestion


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = QuizQuestion
        
        
