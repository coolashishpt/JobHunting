from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Job, Company, Application, SavedJob
from .forms import JobForm, ApplyForm, ApplicationStatusForm
from django.core.paginator import Paginator
from django.db.models import Q


def job_list(request):
    q = request.GET.get('q', '')
    location = request.GET.get('location', '')
    min_salary = request.GET.get('min_salary')
    max_salary = request.GET.get('max_salary')
    job_type = request.GET.get('job_type', '')
    remote = request.GET.get('remote', '')
    skills = request.GET.get('skills', '')

    jobs = Job.objects.filter(is_published=True)

    # Default to Python / Django-focused opportunities unless the user explicitly searches for something else.
    default_python_filter = not any([q, location, min_salary, max_salary, job_type, remote, skills])
    if default_python_filter:
        jobs = jobs.filter(
            Q(title__icontains='python') |
            Q(title__icontains='django') |
            Q(description__icontains='python') |
            Q(description__icontains='django') |
            Q(skills__icontains='python') |
            Q(skills__icontains='django')
        )
    if q:
        jobs = jobs.filter(Q(title__icontains=q) | Q(description__icontains=q) | Q(skills__icontains=q))
    if location:
        jobs = jobs.filter(location__icontains=location)
    if min_salary:
        try:
            jobs = jobs.filter(salary_min__gte=int(min_salary))
        except ValueError:
            pass
    if max_salary:
        try:
            jobs = jobs.filter(salary_max__lte=int(max_salary))
        except ValueError:
            pass
    if job_type:
        jobs = jobs.filter(job_type=job_type)
    if remote in ['true', '1', 'on']:
        jobs = jobs.filter(remote=True)
    if skills:
        # allow comma separated skills
        for s in [s.strip() for s in skills.split(',') if s.strip()]:
            jobs = jobs.filter(skills__icontains=s)

    paginator = Paginator(jobs.order_by('-created_at'), 10)
    page = request.GET.get('page')
    jobs_page = paginator.get_page(page)
    context = {'jobs': jobs_page, 'q': q, 'location': location, 'min_salary': min_salary, 'max_salary': max_salary, 'job_type': job_type, 'remote': remote, 'skills': skills}
    return render(request, 'jobs/job_list.html', context)


def job_detail(request, pk):
    job = get_object_or_404(Job, pk=pk)
    applied = False
    if request.user.is_authenticated:
        applied = Application.objects.filter(job=job, candidate=request.user).exists()
    return render(request, 'jobs/job_detail.html', {'job': job, 'applied': applied})


@login_required
def create_job(request):
    if not getattr(request.user, 'profile', None) or not request.user.profile.role == 'recruiter':
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
def recruiter_dashboard(request):
    if not getattr(request.user, 'profile', None) or request.user.profile.role != 'recruiter':
        return redirect('jobs:job_list')
    jobs = Job.objects.filter(created_by=request.user).order_by('-created_at')
    return render(request, 'jobs/recruiter_dashboard.html', {'jobs': jobs})


@login_required
def candidate_dashboard(request):
    # candidate view: saved jobs and applications
    saved_jobs = SavedJob.objects.filter(user=request.user).select_related('job')
    applications = Application.objects.filter(candidate=request.user).select_related('job')
    return render(request, 'jobs/candidate_dashboard.html', {'saved_jobs': saved_jobs, 'applications': applications})


@login_required
def candidate_application_detail(request, app_pk):
    application = get_object_or_404(Application, pk=app_pk, candidate=request.user)
    return render(request, 'jobs/application_detail_candidate.html', {'application': application})


@login_required
def applicants_list(request, job_pk):
    # recruiter can view applicants for a job they posted
    job = get_object_or_404(Job, pk=job_pk)
    if not getattr(request.user, 'profile', None) or request.user.profile.role != 'recruiter' or job.created_by != request.user:
        return redirect('jobs:job_list')
    applications = Application.objects.filter(job=job).select_related('candidate')
    return render(request, 'jobs/applicants_list.html', {'job': job, 'applications': applications})


@login_required
def applicant_detail(request, job_pk, app_pk):
    job = get_object_or_404(Job, pk=job_pk)
    if not getattr(request.user, 'profile', None) or request.user.profile.role != 'recruiter' or job.created_by != request.user:
        return redirect('jobs:job_list')
    application = get_object_or_404(Application, pk=app_pk, job=job)
    if request.method == 'POST':
        form = ApplicationStatusForm(request.POST, instance=application)
        if form.is_valid():
            prev_status = application.status
            app = form.save()
            # send notification email to candidate if status changed or feedback provided
            # send notification email to candidate via Celery task (non-blocking)
            try:
                from .tasks import send_application_update_email
                subject = f"Update on your application for {job.title}"
                body_lines = [f"Status: {app.get_status_display()}"]
                if app.recruiter_feedback:
                    body_lines.append('\nRecruiter feedback:\n')
                    body_lines.append(app.recruiter_feedback)
                body = "\n".join(body_lines)
                if app.candidate.email:
                    # Use delay to queue the task; task arguments must be JSON-serializable
                    send_application_update_email.delay(subject, body, None, [app.candidate.email])
            except Exception:
                # do not let task/errors block the web request; Celery will log failures
                pass
            return redirect('jobs:applicants_list', job_pk=job.pk)
    else:
        form = ApplicationStatusForm(instance=application)
    return render(request, 'jobs/applicant_detail.html', {'job': job, 'application': application, 'form': form})


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
