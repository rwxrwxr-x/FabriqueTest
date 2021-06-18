from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import NotFound
from django.shortcuts import get_object_or_404
from backend.utils import not_found
from .models import Poll, Question
from .serializers import PollSerializer, QuestionSerializer


class QuestionGetPost(APIView):
    serializer_class = QuestionSerializer
    queryset = Poll.objects.all()

    def get_queryset(self, pk):
        return get_object_or_404(self.queryset, pk=pk)

    def get(self, request, poll_id, *args, **kwargs):
        queryset = self.get_queryset(poll_id).questions

        serializer = self.serializer_class(
            queryset, many=True, context={'request': request}
        )

        return Response(serializer.data)

    def post(self, request, poll_id, *args, **kwargs):
        queryset = self.get_queryset(pk=poll_id)
        serializer = self.serializer_class(
            data=request.data, context={'request': request}
        )
        if serializer.is_valid(raise_exception=True):
            Question.objects.create(poll=queryset, **serializer.data)
            return Response(serializer.data)
        else:
            raise NotFound


class QuestionsDeleteUpdate(APIView):
    serializer_class = QuestionSerializer
    queryset = Poll.objects.all()

    def get_queryset(self, pk):
        return get_object_or_404(self.queryset, pk=pk)

    def put(self, request, question_id):
        serializer_instance = not_found(self.queryset, 'get',
                                        {'pk': question_id})
        serializer = self.serializer_class(
            serializer_instance,
            context={'context': request},
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class PollsViewset(viewsets.ModelViewSet):
    serializer_class = PollSerializer
    queryset = Poll.objects.all()

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
