from django.shortcuts import render
from .models import ErrorChargeModel

def index(request):
    print('comming')
    errors = ErrorChargeModel.objects.all()
    print('commint', errors)
    return render(request, 'index.html', {'errors': errors})