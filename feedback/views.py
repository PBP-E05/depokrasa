import json
from django.shortcuts import render
from django.http import JsonResponse
from .forms import FeedbackForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.http import HttpResponse
from django.core import serializers
from .models import Feedback
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import FeedbackSerializer

@login_required(login_url='authentication:login')
@csrf_exempt
def faq_page(request):
    if request.method == "POST":
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.user = request.user
            feedback.save()
            return JsonResponse({"success": True})
        else:
            return JsonResponse({"success": False, "errors": form.errors})
    else:
        form = FeedbackForm()

    return render(request, 'faq.html', {'form': form})

def show_json(request):
    feedbacks = Feedback.objects.select_related('user').all()
    feedback_list = []
    for feedback in feedbacks:
        feedback_list.append({
            'username': feedback.user.username,
            'email': feedback.user.email if feedback.user.email else '',
            'subject': feedback.subject,
            'message': feedback.message,
            'created_at': feedback.created_at,
        })
    return JsonResponse(feedback_list, safe=False)

@csrf_exempt
def post(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            username = data.get('username')
            subject = data.get('subject')
            message = data.get('message')

            if not username or not subject or not message:
                return JsonResponse({"success": False, "error": "Username, subject, and message are required."}, status=400)

            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                return JsonResponse({"success": False, "error": "User not found."}, status=404)

            feedback_data = {
                'subject': subject,
                'message': message
            }
            form = FeedbackForm(feedback_data)
            if form.is_valid():
                feedback = form.save(commit=False)
                feedback.user = user
                feedback.save()
                return JsonResponse({"success": True, "message": "Feedback submitted successfully!"}, status=201)
            else:
                return JsonResponse({"success": False, "errors": form.errors}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({"success": False, "error": "Invalid JSON data."}, status=400)
    else:
        return JsonResponse({"success": False, "error": "Invalid request method."}, status=405)