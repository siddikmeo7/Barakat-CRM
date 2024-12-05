from django.contrib.auth.views import (
    PasswordResetView as DjangoPasswordResetView,
    PasswordResetDoneView as DjangoPasswordResetDoneView,
    PasswordResetConfirmView as DjangoPasswordResetConfirmView,
    PasswordResetCompleteView as DjangoPasswordResetCompleteView,
    LoginView as DjangoLoginView
)
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from django.http import HttpResponseForbidden
from django.utils.timezone import now, timedelta
from django.views.generic import CreateView
from django.shortcuts import redirect
from Nur.forms import CustomUserForm
from django.contrib.auth.views import LogoutView
from django.core.mail import send_mail

class LoginView(DjangoLoginView):
    template_name = 'registration/login.html'
    fields = '__all__'
    success_url = reverse_lazy('home')

class CustomLogoutView(LogoutView):
    next_page = reverse_lazy("registration/logout")


class UserSignupForm(CreateView):
    form_class = CustomUserForm
    template_name = "registration/signup.html"
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        response = super().form_valid(form)
        user = form.save()
        subject = 'Welcome to Our Website'
        message = f"Hello {user.username},\n\nThank you for registering with us. We are excited to have you on board!"
        from_email = 'NurBussiness@example.com'
        send_mail(subject, message, from_email, [user.email])
        return response

# Password Reset View
class CustomPasswordResetView(PermissionRequiredMixin, DjangoPasswordResetView):
    permission_required = 'auth.change_user'
    template_name = 'registration/password_reset_form.html'
    email_template_name = 'registration/password_reset_email.txt'
    html_email_template_name = 'registration/password_reset_email.html'
    success_url = reverse_lazy('password_reset_done')

    def form_valid(self, form):
        email = form.cleaned_data["email"]
        users = form.get_users(email)
        user = users.first() 

        if user:
            if user.last_password_reset and (now() - user.last_password_reset).total_seconds() < 3600:
                return HttpResponseForbidden("A password reset email has already been sent. Please try again later.")
            user.last_password_reset = now()
            user.save()
        return super().form_valid(form)

# Password Reset Done View
class CustomPasswordResetDoneView(DjangoPasswordResetDoneView):
    template_name = 'registration/custom_password_reset_done.html'

# Password Reset Confirm View
class CustomPasswordResetConfirmView(DjangoPasswordResetConfirmView):
    template_name = 'registration/password_reset_confirm.html'
    success_url = reverse_lazy('password_reset_complete')

    def form_valid(self, form):
        user = form.user
        print(f"Password reset initiated for user: {user.username}")
        response = super().form_valid(form)
        print(f"Password successfully reset for user: {user.username}")
        return response


# Password Reset Complete View
class CustomPasswordResetCompleteView(DjangoPasswordResetCompleteView):
    template_name = 'registration/password_reset_complete.html'




