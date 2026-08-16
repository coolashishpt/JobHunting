from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile


class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)
    role = forms.ChoiceField(choices=Profile.ROLE_CHOICES)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'role')


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['role', 'skills', 'experience_years', 'education', 'resume', 'location', 'portfolio_url', 'company_name', 'company_website']

    def clean_resume(self):
        resume = self.cleaned_data.get('resume')
        if resume:
            if resume.size > 5 * 1024 * 1024:
                raise forms.ValidationError('Resume file is too large (max 5MB)')
            # basic content type check
            valid_mimes = ['application/pdf', 'application/msword', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document']
            if hasattr(resume, 'content_type') and resume.content_type not in valid_mimes:
                raise forms.ValidationError('Unsupported file type')
        return resume
