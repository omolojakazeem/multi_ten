from django import forms
from django.contrib.auth.forms import UserCreationForm

from company.models import Company
from staff.models import Staff


class StaffRegisterationForm(UserCreationForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput())
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput())
    company_name = forms.CharField(label='Company Name')

    class Meta:
        model = Staff
        fields = ['email', 'password1', 'password2', 'company_name']

    def clean(self):
        super(StaffRegisterationForm, self).clean()
        email = self.cleaned_data.get('email')
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        company_name = self.cleaned_data.get('company_name')
        company_exist = Company.objects.filter(company_name=company_name)

        if company_exist.exists():
            self._errors['company_name'] = self.error_class([
                'Company already exist'])

        if email is None:
            self._errors['email'] = self.error_class([
                'Email is required'])

        if company_name is None:
            self._errors['company_name'] = self.error_class([
                'You must enter a company name'])

        if password1 is None:
            self._errors['password1'] = self.error_class([
                'Please enter password'])

        if password2 is None:
            self._errors['password2'] = self.error_class([
                'Please confirm password'])

        if password1 == password2:
            pass
        else:
            self._errors['password2'] = self.error_class([
                'Confirm password must be same as password'])


        return self.cleaned_data


class StaffLoginForm(forms.Form):
    email = forms.CharField(label='Email')
    password = forms.CharField(label='Password', widget=forms.PasswordInput())

    fields = ['email', 'password']

    def clean(self):
        super(StaffLoginForm, self).clean()
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')


        if email is None:
            self._errors['email'] = self.error_class([
                'Email is required'])

        if password is None:
            self._errors['password'] = self.error_class([
                'Password is required to login'])
