# Generated by Django 4.2.7 on 2023-11-23 16:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ChoiceSurvey',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('choice', models.CharField(max_length=100)),
                ('is_answer', models.BooleanField(default=False)),
                ('correct_score', models.IntegerField(default=0)),
                ('incorrect_score', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='QuestionBank',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.TextField()),
                ('question_type', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='QuestionSurvey',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.TextField()),
                ('question_type', models.CharField(max_length=20)),
                ('is_required', models.BooleanField(default=False)),
                ('correct_score', models.IntegerField(default=0)),
                ('incorrect_score', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Survey',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unique_id', models.UUIDField(default=uuid.uuid4, unique=True)),
                ('title', models.CharField(default='Название опроса', max_length=255)),
                ('description', models.TextField(default='Описание опроса')),
                ('is_authentication_required', models.BooleanField(default=False)),
                ('is_quiz', models.BooleanField(default=False)),
                ('create_datetime', models.DateTimeField(auto_now_add=True)),
                ('update_datetime', models.DateTimeField(auto_now=True)),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserSurvey',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.IntegerField(default=0)),
                ('survey', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='forms.survey')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserResponse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('response_text', models.TextField()),
                ('score', models.IntegerField(default=0)),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='forms.questionsurvey')),
                ('selected_options', models.ManyToManyField(to='forms.choicesurvey')),
                ('user_survey', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='responses', to='forms.usersurvey')),
            ],
        ),
        migrations.AddField(
            model_name='questionsurvey',
            name='survey',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='questions', to='forms.survey'),
        ),
        migrations.CreateModel(
            name='CorrectTextAnswerSurvey',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text_answer', models.TextField()),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='correct_text_answers', to='forms.questionsurvey')),
            ],
        ),
        migrations.CreateModel(
            name='CorrectTextAnswerBank',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text_answer', models.TextField()),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='correct_text_answers', to='forms.questionbank')),
            ],
        ),
        migrations.AddField(
            model_name='choicesurvey',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='choices', to='forms.questionsurvey'),
        ),
        migrations.CreateModel(
            name='ChoiceBank',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('choice', models.CharField(max_length=100)),
                ('is_answer', models.BooleanField(default=False)),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='choices', to='forms.questionbank')),
            ],
        ),
    ]
