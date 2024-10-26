from django.shortcuts import render
from django.http import JsonResponse
from .forms import FeedbackForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

@login_required(login_url='authentication:login')
@csrf_exempt
def faq_page(request):
    if request.method == "POST":
        form = FeedbackForm(request.POST)
        if form.is_valid():
            # Process the form (e.g., save feedback)
            return JsonResponse({"success": True})
        else:
            return JsonResponse({"success": False, "errors": form.errors})
    else:
        form = FeedbackForm()

    return render(request, 'faq.html', {'form': form})
