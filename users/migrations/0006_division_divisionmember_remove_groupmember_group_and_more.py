# Generated by Django 4.1.2 on 2023-03-20 06:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.db.models.manager


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_group_groupmember_group_members'),
    ]

    operations = [
        migrations.CreateModel(
            name='Division',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_updated', models.DateTimeField(auto_now=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True, null=True)),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name': 'Division',
                'verbose_name_plural': 'Divisions',
            },
            managers=[
                ('all_objects', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='DivisionMember',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True)),
                ('date_updated', models.DateTimeField(auto_now=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('division', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='members_of_division', to='users.division')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='division_member', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
            managers=[
                ('all_objects', django.db.models.manager.Manager()),
            ],
        ),
        migrations.RemoveField(
            model_name='groupmember',
            name='group',
        ),
        migrations.RemoveField(
            model_name='groupmember',
            name='user',
        ),
        migrations.DeleteModel(
            name='Group',
        ),
        migrations.DeleteModel(
            name='GroupMember',
        ),
        migrations.AddField(
            model_name='division',
            name='members',
            field=models.ManyToManyField(related_name='user_divisions', through='users.DivisionMember', to=settings.AUTH_USER_MODEL),
        ),
    ]