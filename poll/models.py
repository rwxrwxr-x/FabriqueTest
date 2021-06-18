from django.db import models
import datetime


class TimeStampModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(null=True)
    expired = models.BooleanField(default=False)

    class Meta:
        abstract = True

    def set_duration(self, hours):
        self.expires_at = datetime.datetime.utcnow() + datetime.timedelta(hours=hours)


class Poll(TimeStampModel):
    title = models.CharField(max_length=20)
    description = models.CharField(max_length=256)

    def __str__(self):
        return self.title

    class Meta:
        db_table = "polls"


class Question(models.Model):
    poll = models.ForeignKey(Poll, related_name="questions", on_delete=models.CASCADE)
    question = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def vote(self):
        self.votes += 1

    class Meta:
        db_table = "question"
