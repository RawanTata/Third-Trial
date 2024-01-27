from django.db import models

class Exercise(models.Model):
    exercise_id = models.AutoField(primary_key=True)
    description = models.TextField()
    expected_solution = models.TextField()
    generated_solution = models.TextField(blank=True, null=True)  # Field to store AI-generated solution
    evaluation_metrics = models.JSONField(blank=True, null=True)  # Field to store evaluation metrics
    programming_language = models.CharField(max_length=50)
    difficulty_level = models.CharField(max_length=20)
    test_cases = models.JSONField(blank=True, null=True)
