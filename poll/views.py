from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import NotFound
from django.shortcuts import get_object_or_404
from backend.utils import not_found
from .models import Poll, Question, AnonymousUser
from .serializers import (
    PollSerializer,
    QuestionSerializer,
    VoteSerializer,
    VoteSerializerResponse,
    VotedSerializer
)
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticatedOrReadOnly,
    IsAuthenticated,
)


@api_view(["GET"])
@permission_classes([AllowAny])
def active_polls(request):
    queryset = Poll.objects.filter(expired=False).all()
    serializer = PollSerializer(queryset)
    return Response(serializer)


@api_view(["GET"])
@permission_classes([AllowAny])
def voted(request, user_id):
    user = not_found(AnonymousUser, "get", {"pk": user_id})
    serializer = VotedSerializer(user.votes)
    return Response(serializer)


@api_view(["POST"])
@permission_classes([AllowAny])
def upvote(request, poll_id):
    serializer = VoteSerializer(
        data=request.data, context={"request": request, "poll_id": poll_id}
    )
    serializer.is_valid(raise_exception=True)
    res = VoteSerializerResponse(serializer.save()).data
    return Response(res)


class QuestionGetPost(APIView):
    serializer_class = QuestionSerializer
    queryset = Poll.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self, pk):
        return get_object_or_404(self.queryset, pk=pk)

    def get(self, request, poll_id, *args, **kwargs):
        queryset = self.get_queryset(poll_id).questions

        serializer = self.serializer_class(
            queryset, many=True, context={"request": request}
        )

        return Response(serializer.data)

    def post(self, request, poll_id, *args, **kwargs):
        queryset = self.get_queryset(pk=poll_id)
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid(raise_exception=True):
            Question.objects.create(poll=queryset, **serializer.data)
            return Response(serializer.data)
        else:
            raise NotFound


class QuestionsDeleteUpdate(APIView):
    serializer_class = QuestionSerializer
    queryset = Poll.objects.all()
    permission_classes = [IsAuthenticated]

    def get_queryset(self, pk):
        return get_object_or_404(self.queryset, pk=pk)

    def put(self, request, question_id):
        serializer_instance = not_found(self.queryset, "get",
                                        {"pk": question_id})
        serializer = self.serializer_class(
            serializer_instance,
            context={"context": request},
            data=request.data,
            partial=True,
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class PollsViewSet(viewsets.ModelViewSet):
    serializer_class = PollSerializer
    queryset = Poll.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]

    def retrieve(self, request, pk=None, *args, **kwargs):
        queryset = Poll.objects.all()
        poll = get_object_or_404(queryset, pk=pk)
        serializer = self.serializer_class(poll)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer_context = {"request": request}
        serializer = self.serializer_class(
            data=request.data, context=serializer_context
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        pk = kwargs.get("pk", None)
        serializer_context = {"request": request}
        serializer_instance = not_found(self.queryset, "get", {"pk": pk})

        serializer = self.serializer_class(
            serializer_instance,
            context=serializer_context,
            data=request.data,
            partial=True,
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(request.data, status=status.HTTP_200_OK)
