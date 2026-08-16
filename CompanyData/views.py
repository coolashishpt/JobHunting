from django.shortcuts import render
from CompanyData.models import CompanyName

# Public homepage listing companies
def home(request):
    companies = CompanyName.objects.all()
    return render(request, 'index.html', {'companies': companies})
