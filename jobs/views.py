from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Job, Company, Application, SavedJob
from .forms import JobForm, ApplyForm
from django.core.paginator import Paginator
from django.db.models import Q


def job_list(request):
    q = request.GET.get('q', '')
    location = request.GET.get('location', '')
    jobs = Job.objects.filter(is_published=True)
    if q:
        jobs = jobs.filter(Q(title__icontains=q) | Q(description__icontains=q) | Q(skills__icontains=q))
    if location:
        jobs = jobs.filter(location__icontains=location)
    paginator = Paginator(jobs.order_by('-created_at'), 10)
    page = request.GET.get('page')
    jobs_page = paginator.get_page(page)
    return render(request, 'jobs/job_list.html', {'jobs': jobs_page, 'q': q, 'location': location})


def job_detail(request, pk):
    job = get_object_or_404(Job, pk=pk)
    applied = False
    if request.user.is_authenticated:
        applied = Application.objects.filter(job=job, candidate=request.user).exists()
    return render(request, 'jobs/job_detail.html', {'job': job, 'applied': applied})


@login_required
def create_job(request):
    if not request.user.profile.role == 'recruiter':
        return redirect('jobs:job_list')
    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.created_by = request.user
            job.save()
            return redirect('jobs:job_detail', pk=job.pk)
    else:
        form = JobForm()
    return render(request, 'jobs/job_form.html', {'form': form})


@login_required
def apply_job(request, pk):
    job = get_object_or_404(Job, pk=pk)
    if request.method == 'POST':
        form = ApplyForm(request.POST, request.FILES)
        if form.is_valid():
            app = form.save(commit=False)
            app.job = job
            app.candidate = request.user
            app.save()
            return redirect('jobs:job_detail', pk=pk)
    else:
        form = ApplyForm()
    return render(request, 'jobs/apply.html', {'form': form, 'job': job})


@login_required
def save_job(request, pk):
    job = get_object_or_404(Job, pk=pk)
    SavedJob.objects.get_or_create(user=request.user, job=job)
    return redirect('jobs:job_detail', pk=pk)
