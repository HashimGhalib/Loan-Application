from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.views.generic import TemplateView, View

from .forms import UserRegristrationForm


class Home(TemplateView):
    template_name = 'LoanView/home.html'


class Dashboard(TemplateView):
    template_name = 'LoanView/dashboard.html'


class SignUp(View):

    def get(self, request):
        form = UserRegristrationForm()
        context = {
            'form': form
        }
        return render(request, 'LoanView/signup.html', context)

    def post(self, request):
        form = UserRegristrationForm(request.POST)
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

        return render(request, 'LoanView//signup.html', context)



# Create your views here.
