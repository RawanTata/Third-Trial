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

@require_http_methods(["POST"])
@csrf_exempt  # Disable CSRF protection for this view
def generate_and_evaluate(request):
    for exercise in Exercise.objects.all():
        if not exercise.generated_solution:
            # Generate the solution
            exercise.generated_solution = generate_solution(exercise.description)
            exercise.save()

        # Evaluate the solution
        evaluation_result = evaluate_solution(exercise.generated_solution, exercise.expected_solution)
        
        # Update evaluation metrics
        exercise.evaluation_metrics = evaluation_result
        exercise.save()

    return JsonResponse({'status': 'success'})

@api_view(['GET'])
def get_exercise(request, exercise_id):
    exercise = get_object_or_404(Exercise, exercise_id=exercise_id)
    
    if not exercise.generated_solution:
        exercise.generated_solution = generate_solution(exercise.description, 'microsoft/CodeGPT-small-py')
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
