# Generated by Django 2.2.10 on 2021-06-18 13:13

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('poll', '0002_auto_20210618_1252'),
    ]

    operations = [
        migrations.CreateModel(
            name='QuestionAnswers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answers', django.contrib.postgres.fields.jsonb.JSONField()),
            ],
            options={
                'db_table': 'question_answers',
            },
        ),
        migrations.CreateModel(
            name='QuestionTypes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=20)),
            ],
            options={
                'db_table': 'question_types',
            },
        ),
        migrations.AddField(
            model_name='votes',
            name='answer',
            field=models.CharField(default=100, max_length=256),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='votes',
            name='timestamp',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='question',
            name='answers',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='question', to='poll.QuestionAnswers'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='question',
            name='question_type',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='questions_type', to='poll.QuestionTypes'),
            preserve_default=False,
        ),
    ]