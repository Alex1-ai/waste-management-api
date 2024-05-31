from django.http import JsonResponse

# Create your views here.


def home(request):
    return JsonResponse({'info': "Waste-Management-System","Team":"Team Waste Management"})