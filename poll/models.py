from django.db import models
from django.contrib.postgres.fields import JSONField
import datetime


class TimeStampModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(null=True)
    expired = models.BooleanField(default=False)

    class Meta:
        abstract = True

    def set_duration(self, hours):
        self.expires_at = datetime.datetime.utcnow() + datetime.timedelta(
            hours=hours)


class AnonymousUser(models.Model):
    class Meta:
        db_table = 'user'

    def check_question(self, question_id):
        return self.votes.filter(question_id=question_id).all()


class Poll(TimeStampModel):
    title = models.CharField(max_length=20)
    description = models.CharField(max_length=256)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'polls'


class QuestionTypes(models.Model):
    type = models.CharField(max_length=20)

    class Meta:
        db_table = 'question_types'


class QuestionAnswers(models.Model):
    answers = JSONField()

    class Meta:
        db_table = 'question_answers'


class Question(models.Model):
    poll = models.ForeignKey(Poll, related_name='questions',
                             on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def vote(self):
        self.votes += 1

    class Meta:
        db_table = 'question'


class Votes(models.Model):
    user = models.ForeignKey(
        AnonymousUser,
        related_name='votes',
        on_delete=models.CASCADE
    )
    question = models.ForeignKey(
        Question,
        related_name='voted_user',
        on_delete=models.CASCADE
    )
    poll = models.ForeignKey(
        Poll,
        related_name='poll_voted',
        on_delete=models.CASCADE
    )

    class Meta:
        db_table = 'votes'

    def create(self, question, user, poll, /, *args, **kwargs):
        question.vote()
        self.objects.create(question=question,
                            user=user,
                            poll=poll,
                            *args, **kwargs)
