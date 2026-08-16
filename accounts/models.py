from django.conf import settings
from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    ROLE_CHOICES = (
        ('candidate', 'Candidate'),
        ('recruiter', 'Recruiter'),
    )
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='candidate')

    # Candidate fields
    skills = models.TextField(blank=True)
    experience_years = models.PositiveIntegerField(null=True, blank=True)
    education = models.TextField(blank=True)
    resume = models.FileField(upload_to='resumes/', null=True, blank=True)
    location = models.CharField(max_length=200, blank=True)
    portfolio_url = models.URLField(blank=True)

    # Recruiter/company
    company_name = models.CharField(max_length=200, blank=True)
    company_website = models.URLField(blank=True)

    def __str__(self):
        return f"{self.user.username} ({self.role})"
