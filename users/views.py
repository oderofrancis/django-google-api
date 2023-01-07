from django.shortcuts import render,redirect, reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.conf import settings
from django.http import JsonResponse
from django.views.generic.edit import FormView
from django.views.generic import TemplateView
from django.utils.decorators import method_decorator

from django_api.mixins import (
    AjaxFormMixin,
    reCAPTCHAValidation,
    FormErrors,
)

from .forms import (
    UserForm,
    AuthForm,
    UserProfileForm,
)



# Create your views here.

class AccountView(TemplateView):
    '''
    This view is used to render the account page
    '''
    template_name = 'users/account.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(AccountView, self).dispatch(*args, **kwargs)

def ProfileView(request):
    '''
    This view is used to render the profile page
    '''
    User = request.user
    up = User.userprofile

    form = UserProfileForm(instance=up)

    results = 'error'
    message = 'There was an error, please try again later'

    if request.is_ajax():
        form = UserProfileForm(data = request.POST, instance=up)
        if form.is_valid():
            obj = form.save()
            obj.has_profile = True
            obj.save()
            results = 'success'
            message = 'Your profile has been updated'
        else:
            message = FormErrors(form)
        data = {'results': results, 'message': message}

        return JsonResponse(data)
    else:
        context = {'form': form}
        context['google_api_key'] = settings.GOOGLE_API_KEY
        context['base_country'] = settings.BASE_COUNTRY

        return render(request, 'users/profile.html', context)

class SignupView(AjaxFormMixin, FormView):
    '''
    This view is used to render the signup page
    '''
    template_name = 'users/sign_up.html'
    form_class = UserForm
    success_url = '/'

    results = 'Error'
    message = 'There was an error, please try again later'

    # recaptcha key required in context

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["recaptcha_site_key"] = settings.RECAPTCHA_SITE_KEY
        return context

    def form_valid(self, form):
        user = form.save()
        user.set_password(user.password)
        user.save()
        login(self.request, user)
        self.results = 'success'
        self.message = 'Your account has been created'
        return super(SignupView, self).form_valid(form)

    def form_invalid(self, form):
        response = super(SignupView, self).form_invalid(form)
        if self.request.is_ajax():
            message = FormErrors(form)
            return JsonResponse({'results': self.results, 'message': message})
        return response

class LoginView(AjaxFormMixin, FormView):
    '''
    This view is used to render the login page
    '''
    template_name = 'users/login.html'
    form_class = AuthForm
    success_url = '/'

    results = 'Error'
    message = 'There was an error, please try again later'

    def form_valid(self, form):
        user = authenticate(
            username=form.cleaned_data['username'],
            password=form.cleaned_data['password']
        )
        if user is not None:
            login(self.request, user)
            self.results = 'success'
            self.message = 'You have been logged in'
            return super(LoginView, self).form_valid(form)
        else:
            self.message = 'Invalid username or password'
            return super(LoginView, self).form_invalid(form)

    def form_invalid(self, form):
        response = super(LoginView, self).form_invalid(form)
        if self.request.is_ajax():
            message = FormErrors(form)
            return JsonResponse({'results': self.results, 'message': message})
        return response

def LogoutView(request):
    '''
    This view is used to render the logout page
    '''
    logout(request)
    return redirect(reverse('home'))
