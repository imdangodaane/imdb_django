# Generated by Django 2.1.7 on 2019-03-14 07:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('imdb', '0004_comment_target_kind'),
    ]

    operations = [
        migrations.AlterField(
            model_name='actor',
            name='alive',
            field=models.BooleanField(blank=True),
        ),
    ]
