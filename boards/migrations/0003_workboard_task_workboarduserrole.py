# Generated by Django 4.2.16 on 2024-09-27 04:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('boards', '0002_remove_workboard_created_by_delete_task_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='WorkBoard',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(help_text='Title of the Work Board', max_length=255, unique=True)),
                ('description', models.TextField(blank=True, help_text='Optional description of the Work Board', null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='created_boards', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(help_text='Title of the Task', max_length=255)),
                ('description', models.TextField(blank=True, help_text='Optional description of the Task', null=True)),
                ('status', models.CharField(choices=[('ToDo', 'ToDo'), ('In Progress', 'In Progress'), ('Completed', 'Completed')], default='ToDo', max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('assigned_user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='assigned_tasks', to=settings.AUTH_USER_MODEL)),
                ('work_board', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tasks', to='boards.workboard')),
            ],
        ),
        migrations.CreateModel(
            name='WorkBoardUserRole',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.CharField(choices=[('Owner', 'Owner'), ('Collaborator', 'Collaborator'), ('Viewer', 'Viewer')], default='Viewer', max_length=20)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='board_roles', to=settings.AUTH_USER_MODEL)),
                ('work_board', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_roles', to='boards.workboard')),
            ],
            options={
                'unique_together': {('user', 'work_board')},
            },
        ),
    ]
