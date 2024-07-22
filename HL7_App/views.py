from django.shortcuts import render
from .models import ErrorChargeModel

def index(request):
    errors = ErrorChargeModel.objects.all()
    return render(request, 'index.html', {'errors': errors})