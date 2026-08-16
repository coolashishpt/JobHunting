from django.test import TestCase
from django.contrib.auth.models import User
from .models import Company, Job, Application

class RecruiterApplicantTests(TestCase):
    def setUp(self):
        self.recruiter = User.objects.create_user('r', password='r')
        self.recruiter.profile.role = 'recruiter'
        self.recruiter.profile.save()
        self.candidate = User.objects.create_user('c', password='c')
        self.company = Company.objects.create(name='X')
        self.job = Job.objects.create(title='Eng', company=self.company, description='d', is_published=True, created_by=self.recruiter, job_type='full_time')
        self.app = Application.objects.create(job=self.job, candidate=self.candidate, cover_letter='hi')

    def test_recruiter_can_view_applicants(self):
        self.client.force_login(self.recruiter)
        resp = self.client.get(f'/jobs/{self.job.pk}/applicants/')
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'hi')

    def test_recruiter_can_change_status(self):
        self.client.force_login(self.recruiter)
        resp = self.client.post(f'/jobs/{self.job.pk}/applicants/{self.app.pk}/', data={'status': 'reviewing'})
        self.assertEqual(resp.status_code, 302)
        self.app.refresh_from_db()
        self.assertEqual(self.app.status, 'reviewing')

    def test_other_cannot_view(self):
        other = User.objects.create_user('o', password='o')
        other.profile.role = 'recruiter'
        other.profile.save()
        self.client.force_login(other)
        resp = self.client.get(f'/jobs/{self.job.pk}/applicants/')
        # should redirect
        self.assertNotEqual(resp.status_code, 200)
