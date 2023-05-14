# Generated by Django 4.2.1 on 2023-05-14 02:04

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):
    dependencies = [
        ("jar", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="category",
            name="done_verb",
            field=models.CharField(
                help_text="verb, past tense, eg 'Watched'", max_length=50
            ),
        ),
        migrations.AlterField(
            model_name="category",
            name="todo_verb",
            field=models.CharField(help_text="verb, eg 'To Watch'", max_length=50),
        ),
        migrations.AlterField(
            model_name="jaritem",
            name="done_date",
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]
