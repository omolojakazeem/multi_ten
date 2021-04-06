from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views import View

from company.models import Company
from .forms import StaffRegisterationForm, StaffLoginForm
from .models import UserType, Staff

from django.db import connection
from django.urls import reverse
import os


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
            staff.user_type, created = UserType.objects.get_or_create(user_type='Admin')
            
            staff.company = company
            staff.save()
                        
            #set up new schema   

            schema = company.company_domain
            with connection.cursor() as cursor:                        
                cursor.execute(f"CREATE SCHEMA IF NOT EXISTS {schema}")
                cursor.execute(f"SET search_path to {schema}")
                os.system(f'python tenant_context_manage.py {schema} migrate')

            
            #save user also in new schema            
            company = Company.objects.create(company_name=company_name)
            staff = register_form.save(commit=False)
            staff.user_type, created = UserType.objects.get_or_create(user_type='Admin')
            
            staff.company = company
            staff.save()

            #authenticate and login
            my_user = authenticate(request, email=email, password=password)
            login(request, my_user)
            
            
            
            return redirect('http://' + company.company_domain + '.wisemen:8000' + 'account:dashboard')

        else:
            if register_form.errors:
                for field in register_form:
                    for error in field.errors:
                        messages.add_message(request, messages.INFO, error)
            return redirect('account:register_user')


class Dashboard(View):
    template = 'account/profile.html'

    def get(self, request):
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
            with connection.cursor() as cursor:                
                    cursor.execute(f"SET search_path to {request.user.company.company_domain}")

            target = 'http://' + request.user.company.company_domain + '.wisemen:8000/account/dashboard'
            return HttpResponseRedirect(target)
            #return redirect('account:dashboard', request.user.company.company_domain)
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
                target = 'http://' + my_user.company.company_domain + '.wisemen:8000/account/dashboard'
                
                '''
                with connection.cursor() as cursor:                
                    cursor.execute(f"SET search_path to {my_user.company.company_domain}")

                print("SCHEMA", my_user.company.company_domain)
                my_user = authenticate(request, email=email, password=password) 
                '''              
                login(request, my_user)
                return redirect(target)
                
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
