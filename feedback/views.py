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
from django.shortcuts import get_object_or_404, redirect

@login_required(login_url='authentication:login')
@csrf_exempt
def faq_page(request):
    if request.user.is_staff:  # Check if the user is an admin
        feedbacks = Feedback.objects.select_related('user').all()
        return render(request, 'admin_feedback.html', {'feedbacks': feedbacks})
    
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
def edit_feedback(request, feedback_id):
    feedback = get_object_or_404(Feedback, id=feedback_id)
    if request.method == "POST":
        form = FeedbackForm(request.POST, instance=feedback)
        if form.is_valid():
            form.save()
            return redirect('feedback:faq_page')
    else:
        form = FeedbackForm(instance=feedback)
    return render(request, 'edit_feedback.html', {'form': form, 'feedback': feedback})

@csrf_exempt
def delete_feedback(request, feedback_id):
    feedback = get_object_or_404(Feedback, id=feedback_id)
    if request.method == "POST":
        feedback.delete()
        return redirect('feedback:faq_page')
    return render(request, 'confirm_delete.html', {'feedback': feedback})

@csrf_exempt
def submit_feedback_anonymous(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            subject = data.get('subject')
            message = data.get('message')

            if not subject or not message:
                return JsonResponse({"success": False, "error": "Subject and message are required."}, status=400)

            feedback_data = {
                'subject': subject,
                'message': message
            }
            form = FeedbackForm(feedback_data)
            if form.is_valid():
                feedback = form.save(commit=False)
                feedback.user = None  # Atur pengguna ke None untuk anonim
                feedback.save()
                return JsonResponse({"success": True, "message": "Feedback submitted successfully!"}, status=201)
            else:
                return JsonResponse({"success": False, "errors": form.errors}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({"success": False, "error": "Invalid JSON data."}, status=400)
    else:
        return JsonResponse({"success": False, "error": "Invalid request method."}, status=405)