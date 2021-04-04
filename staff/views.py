from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect
from django.views import View

from company.models import Company
from .forms import StaffRegisterationForm, StaffLoginForm
from .models import UserType, Staff


class RegisterUser(View):
    template = 'account/register.html'

    def get(self, request):
        register_form = StaffRegisterationForm()
        context = {
            'register_form': register_form
        }
        return render(request, template_name=self.template, context=context)

    def post(self, request):
        register_form = StaffRegisterationForm(request.POST)

        if register_form.is_valid():

            email = register_form.cleaned_data['email']
            password = register_form.cleaned_data['password1']
            password2 = register_form.cleaned_data['password2']
            company_name = register_form.cleaned_data['company_name']


            company = Company.objects.create(company_name=company_name)
            staff = register_form.save(commit=False)
            staff.user_type = UserType.objects.get(user_type='Admin')
            staff.company = company
            staff.save()
            my_user = authenticate(request, email=email, password=password)
            login(request, my_user)
            return redirect('account:dashboard', domain=request.user.company.company_domain)

        else:
            if register_form.errors:
                for field in register_form:
                    for error in field.errors:
                        messages.add_message(request, messages.INFO, error)
            return redirect('account:register_user')


class Dashboard(View):
    template = 'account/profile.html'

    def get(self, request,domain):
        try:
            # Retrieve the user account associated with the current subdomain.
            staff = Staff.objects.get(company__company_domain=request.user.company.company_domain)
        except Staff.DoesNotExist:
            # No user matches the current subdomain, so return a generic 404.
            raise Http404

        context = {
            'staff':staff,

        }
        return render(request, template_name=self.template, context=context)


class LoginUser(View):
    template = 'account/login.html'

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('account:dashboard', request.user.company.company_domain)
        login_form = StaffLoginForm()
        context = {
            'login_form': login_form,
        }
        return render(request, template_name=self.template, context=context)

    def post(self, request):
        login_form = StaffLoginForm(request.POST)
        if login_form.is_valid():
            email = login_form.cleaned_data['email']
            password = login_form.cleaned_data['password']
            my_user = authenticate(request, email=email, password=password)

            if my_user is not None:
                login(request, my_user)
                return redirect('account:dashboard', request.user.company.company_domain)
            else:
                print(login_form.errors)
                messages.add_message(
                    request, messages.INFO,
                    'Email / Password')
                return redirect('account:login_user')
        else:
            print(login_form.errors)
            messages.add_message(request, messages.INFO, 'Error in form')
            return redirect('account:login_user')


class LogoutUser(View):
    def get(self,request):
        logout(request)
        return redirect('account:register_user')
