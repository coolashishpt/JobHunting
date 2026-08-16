from django.test import TestCase
from django.contrib.auth.models import User
from .models import Company, Job, Application


class JobsTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('recruiter', password='rpass')
        # ensure profile exists and mark as recruiter
        self.user.profile.role = 'recruiter'
        self.user.profile.save()
        self.company = Company.objects.create(name='Acme')

    def test_create_job(self):
        self.client.force_login(self.user)
        resp = self.client.post('/jobs/create/', data={
            'title': 'Engineer', 'company': self.company.id, 'description': 'Do stuff', 'is_published': True, 'job_type': 'full_time'
        })
        self.assertEqual(resp.status_code, 302)
        self.assertTrue(Job.objects.filter(title='Engineer').exists())

    def test_apply_job(self):
        candidate = User.objects.create_user('cand', password='cpass')
        job = Job.objects.create(title='T', company=self.company, description='d', is_published=True)
        self.client.force_login(candidate)
        resp = self.client.post(f'/jobs/{job.pk}/apply/', data={'cover_letter': 'Hi'})
        self.assertEqual(resp.status_code, 302)
        self.assertTrue(Application.objects.filter(job=job, candidate=candidate).exists())
