from django.shortcuts import render
from . forms import registrationForm
from django.contrib import messages
from django.views.generic.edit import FormView
from django.views.generic.base import View
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from .tokens import email_token_generator


class regForm(FormView):
    template_name = "index.html"
    form_class = registrationForm
    success_url = "/"

    def get_initial(self):
        initial = super().get_initial()
        initial["name"] = "Name"
        initial["description"] = "Description"
        return initial

    def form_valid(self, form):
        name = form.cleaned_data["name"]
        description = form.cleaned_data["description"]
        email = form.cleaned_data["email"]

        if form.has_changed():
            password = form.cleaned_data["password"]
            if password == "yamete..//2023.888":
                email_this = {
                    "name": name,
                    "description": description,
                }
                send_password_reset_link(self.request, email_this, email)
                messages.success(self.request, (name, description))
                return super().form_valid(form)
            else:
                messages.warning(self.request, "Incorrect password.")
                return self.form_invalid(form)
        else:
            messages.success(self.request, "No changes in the form.")
            return super().form_valid(form)


# This function will create the reset link
def send_password_reset_link(request, dct, email):
    mail_subject = "Email Message"
    message = render_to_string("email.html", {
        "dct": dct["name"],
        "domain": get_current_site(request).domain,
        "name": urlsafe_base64_encode(force_bytes(dct["name"])),
        "description": urlsafe_base64_encode(force_bytes(dct["description"])),
        "token": email_token_generator.make_token(dct),
        "protocol": "https" if request.is_secure() else "http"
    })
    email = EmailMessage(mail_subject, message, to=[email])

    if email.send():
        messages.success(
            request, f"An email link is sent.")
    else:
        messages.error(
            request, f"An email link did not sent.")


class password_reset_form(View):

    def get(self, request, *args, **kwargs):

        context = {
            "first": "<script>alert('hello')</script>"
        }

        dct = {
            "name": force_str(urlsafe_base64_decode(self.kwargs['name'])),
            "description": force_str(urlsafe_base64_decode(self.kwargs['description'])),
        }

        if email_token_generator.check_token(dct, self.kwargs['token']):
            messages.success(
                request, "Token is still valid.")
        else:
            messages.error(request, "Reset token is no longer valid.")

        return render(request, "here.html", context)
