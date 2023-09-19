# Generated by Django 4.1.7 on 2023-09-14 18:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_userinputs'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userinputs',
            name='phone_number',
        ),
        migrations.AddField(
            model_name='userinputs',
            name='username',
            field=models.CharField(default=1, max_length=20),
            preserve_default=False,
        ),
    ]