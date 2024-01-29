from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render

# Create your views here.
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Exercise
from .utils import generate_solution
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from .utils import evaluate_solution


def home(request):
    # Add logic for your home view
 #   return render(request, 'home.html')  # Ensure you have a template named 'home.html'
    return render(request, 'code_evaluator/home.html')


# Define your model checkpoints
MODEL_1_CHECKPOINT = 'EleutherAI/gpt-neo-1.3B'
MODEL_2_CHECKPOINT = 'microsoft/CodeGPT-small-py'

@require_http_methods(["POST"])
@csrf_exempt
def generate_and_evaluate(request):
    results = {}
    for exercise in Exercise.objects.all():
        solution_1 = generate_solution(exercise.description, MODEL_1_CHECKPOINT)
        solution_2 = generate_solution(exercise.description, MODEL_2_CHECKPOINT)

        results[exercise.id] = {
            'solution_1': evaluate_solution(solution_1, exercise.expected_solution),
            'solution_2': evaluate_solution(solution_2, exercise.expected_solution)
        }
    return JsonResponse(results)


@api_view(['GET'])
def get_exercise(request, exercise_id):
    exercise = get_object_or_404(Exercise, exercise_id=exercise_id)

    if not exercise.generated_solution:
        exercise.generated_solution = generate_solution(
            exercise.description)
        exercise.save()

    # Simple evaluation (can be enhanced)
    exercise.evaluation_metrics = {
        'match': exercise.generated_solution == exercise.expected_solution
    }
    exercise.save()

    data = {
        'exercise_id': exercise.exercise_id,
        'description': exercise.description,
        'expected_solution': exercise.expected_solution,
        'generated_solution': exercise.generated_solution,
        'evaluation_metrics': exercise.evaluation_metrics,
        'programming_language': exercise.programming_language,
        'difficulty_level': exercise.difficulty_level,
    }
    return Response(data)
