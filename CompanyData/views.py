from django.db.models import Q
from django.shortcuts import render
from CompanyData.models import CompanyName

# Public homepage listing companies relevant to Python / Django hiring
PYTHON_DJANGO_KEYWORDS = ('python', 'django')

def home(request):
    q = Q()
    for keyword in PYTHON_DJANGO_KEYWORDS:
        q |= Q(company_name__icontains=keyword) | Q(career_page__icontains=keyword)

    companies = CompanyName.objects.filter(q).distinct()
    return render(request, 'index.html', {'companies': companies})
