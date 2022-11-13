from django.urls import path
from . views import regForm, password_reset_form

app_name = "home"

urlpatterns = [
    path("", regForm.as_view(), name="index"),
    path("email_confirmed/<name>/<description>/<token>/",
         password_reset_form.as_view(), name="emailconfirmed"),
]
