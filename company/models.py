from django.db import models

# Create your models here.
from django.utils.text import slugify


def get_domain(company_name):
    domain = company_name.lower().split(' ')
    return domain[0]


class Company(models.Model):
    
    SUPER_DOMAIN = "wisemen"

    company_name = models.CharField(max_length=100,)
    company_host = models.CharField(max_length=50, blank=True, null=True)
    company_domain = models.CharField(max_length=20,blank=True, null=True)
    company_slug = models.SlugField(null=True, blank=True)
    company_address = models.TextField(null=True, blank=True)
    company_email = models.EmailField(null=True, blank=True)
    company_email_cc = models.EmailField(blank=True, null=True)
    company_phone = models.CharField(max_length=30, null=True, blank=True)
    company_RC = models.CharField(max_length=20, blank=True, null=True)
    company_registered_on = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.company_slug = slugify(self.company_name)
        self.company_domain = get_domain(self.company_name)
        self.company_host = self.company_domain + self.SUPER_DOMAIN
        super(Company, self).save(*args, **kwargs)

    def __str__(self):
        return self.company_name
