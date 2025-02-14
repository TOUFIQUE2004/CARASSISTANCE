from django.shortcuts import render
from django.http import JsonResponse

def home(request):
    return render(request, 'assistant/home.html')

def get_voice_query(request):
    # Placeholder response for testing purposes
    response = {"message": "Voice query functionality is under development."}
    return JsonResponse(response)
