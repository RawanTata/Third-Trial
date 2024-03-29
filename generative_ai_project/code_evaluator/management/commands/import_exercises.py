import json
from django.core.management.base import BaseCommand
from code_evaluator.models import Exercise

class Command(BaseCommand):
    help = 'Import exercises from a JSON file'

    def add_arguments(self, parser):
        parser.add_argument('json_file', type=str, help='Path to JSON file with exercises')

    def handle(self, *args, **kwargs):
        with open(kwargs['json_file'], 'r') as file:
            exercises = json.load(file)
            for ex in exercises:
                Exercise.objects.create(
                    description=ex['description'],
                    expected_solution=ex['expected_solution'],
                    programming_language=ex['programming_language'],
                    difficulty_level=ex['difficulty_level']
                )
                self.stdout.write(self.style.SUCCESS(f"Imported: {ex['description']}"))
