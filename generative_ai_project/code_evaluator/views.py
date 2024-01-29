from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render

# Create your views here.
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import NewExercise
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
    for NewExercise in NewExercise.objects.all():
        solution_1 = generate_solution(NewExercise.description, MODEL_1_CHECKPOINT)
        solution_2 = generate_solution(NewExercise.description, MODEL_2_CHECKPOINT)

        results[NewExercise.id] = {
            'solution_1': evaluate_solution(solution_1, NewExercise.expected_solution),
            'solution_2': evaluate_solution(solution_2, NewExercise.expected_solution)
        }
    return JsonResponse(results)


@api_view(['GET'])
def get_NewExercise(request, NewExercise_id):
    NewExercise = get_object_or_404(NewExercise, NewExercise_id=NewExercise_id)

    if not NewExercise.generated_solution:
        NewExercise.generated_solution = generate_solution(
            NewExercise.description)
        NewExercise.save()

    # Simple evaluation (can be enhanced)
    NewExercise.evaluation_metrics = {
        'match': NewExercise.generated_solution == NewExercise.expected_solution
    }
    NewExercise.save()

    data = {
        'NewExercise_id': NewExercise.NewExercise_id,
        'description': NewExercise.description,
        'expected_solution': NewExercise.expected_solution,
        'generated_solution': NewExercise.generated_solution,
        'evaluation_metrics': NewExercise.evaluation_metrics,
        'programming_language': NewExercise.programming_language,
        'difficulty_level': NewExercise.difficulty_level,
    }
    return Response(data)
