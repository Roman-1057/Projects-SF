# Generated by Django 4.1.3 on 2023-10-23 16:58

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('news', '0006_alter_author_user_alter_comment_post'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='subscribers',
            field=models.ManyToManyField(related_name='subscribed_categories', to=settings.AUTH_USER_MODEL),
        ),
    ]
