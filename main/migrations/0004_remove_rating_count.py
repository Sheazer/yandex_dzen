# Generated by Django 4.2.19 on 2025-03-04 12:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_remove_post_description_comment_comment_post_text_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='rating',
            name='count',
        ),
    ]
