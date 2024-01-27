# Generated by Django 5.0.1 on 2024-01-27 17:51

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Exercise',
            fields=[
                ('exercise_id', models.AutoField(primary_key=True, serialize=False)),
                ('description', models.TextField()),
                ('expected_solution', models.TextField()),
                ('generated_solution', models.TextField(blank=True, null=True)),
                ('evaluation_metrics', models.JSONField(blank=True, null=True)),
                ('programming_language', models.CharField(max_length=50)),
                ('difficulty_level', models.CharField(max_length=20)),
            ],
        ),
    ]
