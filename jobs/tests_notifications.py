from django.test import TestCase, override_settings
from django.contrib.auth.models import User
from .models import Company, Job, Application
from django.core import mail

@override_settings(EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend')
class NotificationTests(TestCase):
    def setUp(self):
        self.recruiter = User.objects.create_user('r2', password='r')
        self.recruiter.profile.role = 'recruiter'
        self.recruiter.profile.save()
        self.candidate = User.objects.create_user('c2', email='c2@example.com', password='c')
        self.company = Company.objects.create(name='Y')
        self.job = Job.objects.create(title='Eng2', company=self.company, description='d', is_published=True, created_by=self.recruiter, job_type='full_time')
        self.app = Application.objects.create(job=self.job, candidate=self.candidate, cover_letter='hello')

    def test_email_sent_on_status_change(self):
        self.client.force_login(self.recruiter)
        resp = self.client.post(f'/jobs/{self.job.pk}/applicants/{self.app.pk}/', data={'status': 'reviewing', 'recruiter_feedback': 'Looks good'})
        self.assertEqual(resp.status_code, 302)
        # one email should be sent
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn('Update on your application', mail.outbox[0].subject)
        self.app.refresh_from_db()
        self.assertEqual(self.app.status, 'reviewing')
        self.assertEqual(self.app.recruiter_feedback, 'Looks good')
