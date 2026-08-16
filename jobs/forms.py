from django import forms
from .models import Job, Application


class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['title', 'company', 'description', 'location', 'salary_min', 'salary_max', 'job_type', 'remote', 'experience_level', 'skills', 'is_published']


class ApplyForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['cover_letter', 'resume']

    def clean_resume(self):
        resume = self.cleaned_data.get('resume')
        if resume:
            if resume.size > 5 * 1024 * 1024:
                raise forms.ValidationError('Resume file is too large (max 5MB)')
        return resume


class ApplicationStatusForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['status', 'recruiter_feedback']
        widgets = {
            'recruiter_feedback': forms.Textarea(attrs={'rows': 4}),
        }
