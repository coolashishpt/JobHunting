from django.db import models

# Create your models here.

class CompanyName(models.Model):
    company_name = models.CharField(max_length=100)
    career_page = models.CharField(max_length=500)
    employee_strength = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.company_name