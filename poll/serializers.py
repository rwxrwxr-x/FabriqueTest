from rest_framework import serializers
from .models import Poll, Question


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ["id", "question"]


class PollSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True)

    class Meta:
        model = Poll
        fields = [
            "id",
            "title",
            "description",
            "questions",
            "created_at",
            "expires_at",
            "expired",
        ]
        read_only = ["created_at"]

    def create(self, validated_data, *args, **kwargs):
        questions = validated_data.pop("questions")
        poll = Poll.objects.create(**validated_data)
        for question in questions:
            Question.objects.create(poll=poll, **question)

        return poll

    def update(self, instance, validated_data):
        validated_data.pop("questions", None)
        Poll.objects.filter(pk=instance.pk).update(**validated_data)
        return instance
