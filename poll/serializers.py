from rest_framework import serializers
from .models import Poll, Question, Votes, AnonymousUser
from rest_framework.exceptions import PermissionDenied
from backend.utils import not_found


class QuestionSerializer(serializers.ModelSerializer):
    votes = serializers.ReadOnlyField()
    type = serializers.SerializerMethodField("get_type_text")
    answers = serializers.JSONField()

    @staticmethod
    def get_type_text(obj):
        return obj.question_type.type

    class Meta:
        model = Question
        fields = ["id", "question", "votes", "question_type", "type",
                  "answers"]


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


class VoteSerializer(serializers.Serializer):
    question_id = serializers.IntegerField(required=True)
    user_id = serializers.IntegerField(required=False)
    answer = serializers.CharField(required=True)

    def create(self, validated_data):
        question_id = validated_data.get("question_id")
        question = not_found(Question, "get", {"pk": question_id})
        answer = validated_data.get("answer")
        if question.poll.expired:
            raise PermissionDenied("Poll expired!")
        if pk := validated_data.get("user_id", None):
            user = AnonymousUser.objects.get(pk=pk)
            if user.votes.filter(question_id=question_id).all():
                raise PermissionDenied("User already vote")
        else:
            user = AnonymousUser.objects.create()
        vote = Votes.objects.create(question=question, user=user,
                                    poll=question.poll,
                                    answer=answer)
        return vote

    def update(self, instance, validated_data):
        pass


class VoteSerializerResponse(serializers.ModelSerializer):
    question = QuestionSerializer()
    poll_id = serializers.IntegerField()
    user_id = serializers.IntegerField()
    timestamp = serializers.DateTimeField()
    answer = serializers.CharField()

    class Meta:
        model = Votes
        fields = ["question", "user_id", "poll_id","answer", "timestamp"]


class VotedSerializer(serializers.ModelSerializer):
    question = QuestionSerializer()
    poll = PollSerializer()
    user_id = serializers.IntegerField()
    answer = serializers.CharField()

    class Meta:
        model = Votes
        fields = ['user_id', 'poll', 'question', 'answer']
