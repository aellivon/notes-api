# Generated by Django 4.1.2 on 2023-06-15 01:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='groupprofile',
            options={'verbose_name': 'Group Profile', 'verbose_name_plural': 'Group Profiles'},
        ),
        migrations.RenameField(
            model_name='groupprofile',
            old_name='created',
            new_name='created_at',
        ),
        migrations.RenameField(
            model_name='groupprofile',
            old_name='date_updated',
            new_name='updated_at',
        ),
        migrations.RenameField(
            model_name='user',
            old_name='created',
            new_name='created_at',
        ),
        migrations.RenameField(
            model_name='user',
            old_name='date_updated',
            new_name='updated_at',
        ),
        migrations.AlterField(
            model_name='user',
            name='date_joined',
            field=models.DateTimeField(null=True),
        ),
    ]
