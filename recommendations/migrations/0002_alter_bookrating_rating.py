# Generated by Django 5.1.1 on 2025-04-16 12:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recommendations', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookrating',
            name='rating',
            field=models.CharField(choices=[('like', '👍 Me gusta'), ('dislike', '👎 No me gusta')], max_length=7),
        ),
    ]
