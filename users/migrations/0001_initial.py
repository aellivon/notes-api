# Generated by Django 4.1.2 on 2023-06-17 12:16

from django.db import migrations, models
import django.db.models.deletion
import django.db.models.manager
import users.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='GroupProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('group', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='auth.group')),
            ],
            options={
                'verbose_name': 'Group Profile',
                'verbose_name_plural': 'Group Profiles',
                'abstract': False,
            },
            managers=[
                ('all_objects', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('is_active', models.BooleanField(default=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('first_name', models.CharField(max_length=225)),
                ('last_name', models.CharField(max_length=225)),
                ('email', models.EmailField(max_length=500, unique=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('furigana_fname', models.CharField(blank=True, default='', max_length=100)),
                ('furigana_lname', models.CharField(blank=True, default='', max_length=100)),
                ('position', models.CharField(blank=True, default='', max_length=100)),
                ('avatar_url', models.ImageField(blank=True, null=True, upload_to=users.models.profile_directory_path)),
                ('date_joined', models.DateTimeField(null=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
