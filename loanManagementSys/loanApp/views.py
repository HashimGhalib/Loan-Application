import json

import requests
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.html import strip_tags
from django.views.generic import TemplateView, View, CreateView, UpdateView, DeleteView

from . import sendpulse_service
from .forms import UserRegForm, BorrowerForm, LoanApplicationForm

import uuid
from urllib.parse import urlencode

from django.conf import settings
# from ..loanManagementSys import settings
from .models import Borrower, LoanApplication


class Home(LoginRequiredMixin, TemplateView):
    template_name = 'LoanView/home.html'


class SignUp(View):
    def get(self, request):
        form = UserRegForm()
        context = {
            'form': form
        }
        return render(request, 'LoanView/signup.html', context)

    def post(self, request):
        form = UserRegForm(request.POST)
        context = {
            'form': form
        }
        if form.is_valid():
            form.save()
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password1']
            )
            login(request, user)
            return redirect('dashboard')
        return render(request, 'LoanView/signup.html', context)


class Dashboard(LoginRequiredMixin, View):
    template_name = 'LoanView/dashboard.html'

    def get(self, request):
        try:
            template_name = 'LoanView/dashboard.html'
            # loan_application_id = request.session.get('loan_application_id')
            # if loan_application_id is None:
            #     return redirect('application')
            # loan_application_id_dict = json.loads(loan_application_id)
            # loan_application_id_dict_value = loan_application_id_dict['id']
            borrowers = Borrower.objects.get(user=self.request.user.id)
            b_id = borrowers.borrower_id
            loanApp = LoanApplication.objects.get(borrower=b_id)

            context = {'loanApp': loanApp}
            return render(request, template_name, context)
        except LoanApplication.DoesNotExist:
            return redirect('application')


class BorrowerProfile(LoginRequiredMixin, View):
    def get(self, request):
        try:
            borrowers = Borrower.objects.get(user=self.request.user.id)
            context = {'borrowers': borrowers}
            return render(request, 'LoanView/borrower-profile.html', context)
        except Borrower.DoesNotExist:
            return redirect('add-borrower')


class AddBorrower(LoginRequiredMixin, CreateView):
    model = Borrower
    form_class = BorrowerForm
    template_name = 'LoanView/borrower.html'
    success_url = reverse_lazy('application')

    def form_valid(self, form):
        form.instance.user = self.request.user
        # borrow = form.save(commit=False)
        # data = {'id': str(borrow.borrower_id)}
        # self.request.session['borrower_id'] = json.dumps(data)
        # borrow.save()
        return super().form_valid(form)


class EditBorrower(LoginRequiredMixin, UpdateView):
    model = Borrower
    form_class = BorrowerForm
    template_name = 'LoanView/borrower.html'
    success_url = reverse_lazy('borrower-profile')


class DeleteBorrower(LoginRequiredMixin, DeleteView):
    model = Borrower
    # form_class = BorrowerForm
    template_name = 'LoanView/delete-borrower.html'
    success_url = reverse_lazy('dashboard')
    context_object_name = "form"


# LOAN APPLICATION
class LoanApp(LoginRequiredMixin, View):
    def get(self, request):
        form = LoanApplicationForm()
        return render(request, 'LoanView/loan_application.html', {'form': form})

    def post(self, request):
        form = LoanApplicationForm(request.POST)
        borrowers = Borrower.objects.get(user=self.request.user.id)
        borrowerID = borrowers.borrower_id
        borrower = get_object_or_404(Borrower, pk=borrowerID)

        if form.is_valid():
            loan_application = form.save(commit=False)  # Don't save to the database yet
            loan_application.borrower = borrower  # Set the borrower
            # data = {'id': str(loan_application.loan_application_id)}
            # request.session['loan_application_id'] = json.dumps(data)
            loan_application.save()  # Save to the database
            return redirect('dashboard')
        return render(request, 'LoanView/loan_application.html', {'form': form, 'borrower': borrower})


class LoanAppDelete(LoginRequiredMixin, DeleteView):
    model = LoanApplication
    template_name = 'LoanView/delete-application.html'
    success_url = reverse_lazy('home')
    # context_object_name = 'form'



    #
    # def put(self, request, pk):
    #     # Retrieve the LoanApplication instance or return a 404 error if not found
    #     loan_application = get_object_or_404(LoanApplication, pk=pk)
    #
    #     if request.method == 'POST':
    #         form = LoanApplicationForm(request.POST, instance=loan_application)
    #         if form.is_valid():
    #             form.save()  # Save changes to the database
    #             return redirect('loan_application_detail', pk=pk)  # Redirect to a success page or detail view


# LOAN REPAYMENT
class LoanRepayment(View):
    def get(self, request):
        form = LoanApplicationForm()
        return render(request, 'loan_repayment.html', {'form': form})

    def post(self, request):
        form = LoanApplicationForm(request.POST)

        loan_amount = request.POST.get('loan_amount')  # Principal
        interest_rate = request.POST.get('interest_rate')  # Interest Rate
        loan_term = request.POST.get('loan_term')  # Loan Term

        interest = (loan_amount * (interest_rate / 100) * (loan_term / 12))

        context = {
            'form': form,
            'interest': interest
        }

        if form.is_valid():
            form.save()
            return redirect('dashboard')
        return render(request, 'loan_repayment.html', context)










        # def generate_verification_link(self, user_id):
    #     token = str(uuid.uuid4())
    #     verification_link = f'https://yourdomain.com/verify?{urlencode({"user_id": user_id, "token": token})}'
    #     return verification_link

    # def post(self, request):
    #     if request.method == 'POST':
    #         form = UserRegForm(request.POST)
    #         context = {
    #                 'form': form
    #             }
    #         if form.is_valid():
    #             user = form.save(commit=False)
    #             user.is_active = False  # Deactivate account until email is confirmed
    #             user.save()
    #             # current_site = get_current_site(request)
    #             mail_subject = 'Activate your account.'
    #             html_content = f"""
    #                                     Email Verification
    #                                     Hi, {user.username}
    #                                     Please verify your email by clicking the link below:
    #                                     Verify your email
    #                                     If you did not create an account, please ignore this email.
    #                                     Best regards,<br>Your Company
    #                              """

                # message = html_content
                # # msg = strip_tags(message)
                # send_mail(mail_subject,
                #             message,
                #             settings.EMAIL_HOST_USER, # From Email,
                #             [user.email],
                #           fail_silently=False
                #           )
                # usr = authenticate(
                #                 email=form.cleaned_data['email'],
                #                 password=form.cleaned_data['password']
                #             )
                # if user is not None:
        #         user.is_active = True
        #         user.save()
        #         login(request, usr)
        #             # return HttpResponse('Success')
        #         return redirect('dashboard')
        #     return render(request, 'LoanView/signup.html', context)
        #
        # else:
        #     form = UserRegForm()
        #     context = {'form': form}
        #     return render(request, 'LoanView/signup.html', context)

        # form = UserRegForm(request.POST)
        # context = {
        #     'form': form
        # }
        #
        # if form.is_valid():
        #     form.save()
        #
        #     email = request.POST.get('email')
        #     email2 = User.objects.get('email')
        #     user_id = User.objects.get('id')
        #
        #     verification_link = self.generate_verification_link(user_id)
        #
        #     subject = 'Activate Your Account'
        #     html_content = f"""
        #                 <html>
        #                 <body>
        #                     <h2>Email Verification</h2>
        #                     <p>Hi, {user_id.username}</p>
        #                     <p>Please verify your email by clicking the link below:</p>
        #                     <p><a href="{verification_link}">Verify your email</a></p>
        #                     <p>If you did not create an account, please ignore this email.</p>
        #                     <p>Best regards,<br>Your Company</p>
        #                 </body>
        #                 </html>
        #                 """

            # send_mail(
            #         subject=subject, # Subject
            #         message=render_to_string(html_content), # message
            #         from_email=settings.EMAIL_HOST_USER, # From Email
            #         recipient_list=[email2], # To Email
            #         fail_silently=False
            #         )

        #     user = authenticate(
        #                 email=form.cleaned_data['email'],
        #                 password=form.cleaned_data['password']
        #             )
        #     login(request, user)
        #     return redirect('dashboard')
        #
        # return render(request, 'LoanView/signup.html', context)



