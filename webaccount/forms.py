import unicodedata
from django import forms
from django.contrib.auth import (
    authenticate, get_user_model, password_validation,
)
from django.contrib.auth.hashers import (
    UNUSABLE_PASSWORD_PREFIX, identify_hasher,
)
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMultiAlternatives
from django.template import loader
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.utils.text import capfirst
from django.utils.translation import gettext, gettext_lazy as _
from django.conf import settings
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.shortcuts import render,redirect
from django.contrib import messages
UserModel = get_user_model()




class ReadOnlyPasswordHashWidget(forms.Widget):
    template_name = 'auth/widgets/read_only_password_hash.html'
    read_only = True

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        summary = []
        if not value or value.startswith(UNUSABLE_PASSWORD_PREFIX):
            summary.append({'label': gettext("No password set.")})
        else:
            try:
                hasher = identify_hasher(value)
            except ValueError:
                summary.append({'label': gettext("Invalid password format or unknown hashing algorithm.")})
            else:
                for key, value_ in hasher.safe_summary(value).items():
                    summary.append({'label': gettext(key), 'value': value_})
        context['summary'] = summary
        return context


class ReadOnlyPasswordHashField(forms.Field):
    widget = ReadOnlyPasswordHashWidget

    def __init__(self, *args, **kwargs):
        kwargs.setdefault("required", False)
        super().__init__(*args, **kwargs)

    def bound_data(self, data, initial):
        # Always return initial because the widget doesn't
        # render an input field.
        return initial

    def has_changed(self, initial, data):
        return False




class UsernameField(forms.CharField):
    def to_python(self, value):
        return unicodedata.normalize('NFKC', super().to_python(value))


class UserCreationForm(forms.ModelForm):
    """
    A form that creates a user, with no privileges, from the given username and
    password.
    """
    error_messages = {
        'password_mismatch': _("The two password fields didn't match."),
    }
    email = forms.CharField(
        label=_("Email"),
        # strip=False,
        widget=forms.EmailInput,
        # help_text=password_validation.password_validators_help_text_html(),
    )
    # password2 = forms.CharField(
    #     label=_("Password confirmation"),
    #     widget=forms.PasswordInput,
    #     strip=False,
    #     help_text=_("Enter the same password as before, for verification."),
    # )

    class Meta:
        model = User
        fields = ("username",)
        field_classes = {'username': UsernameField}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self._meta.model.USERNAME_FIELD in self.fields:
            self.fields[self._meta.model.USERNAME_FIELD].widget.attrs.update({'autofocus': True})

    # def clean_username(self):
    #     # password1 = self.cleaned_data.get("password1")
    #     # password2 = self.cleaned_data.get("password2")
    #     # if password1 and password2 and password1 != password2:
    #     #     raise forms.ValidationError(
    #     #         self.error_messages['password_mismatch'],
    #     #         code='password_mismatch',
    #     #     )
    #     # return password2
    #     if self.cleaned_data.get("username") == '':
    #         raise forms.ValidationError("Username is empty")
    #     return self.cleaned_data.get("username")

    # def clean(self):
    #     clean_data = self.cleaned_data
    #     if clean_data.get("username") == '':
    #         raise forms.ValidationError("Error")
    #     return clean_data

    # def clean_username(self):
    #     data = self.cleaned_data.get("username")
    #     if data is None:
    #         forms.ValueError("sdjfnkjsdnfkjsdf")
    #     return data

    def _post_clean(self):
        try:
            # clean_data = self.cleaned_data
            # if clean_data.get("username") == '':
            #     raise forms.ValidationError("Error")
            super()._post_clean()
        except:
            return redirect("/auth/user/add/")
        # Validate the password after self.instance is updated with form data
        # by super().
        # if self.cleaned_data.get("passw")
        mail_subject = "Password Set Link"
        to_email = self.cleaned_data.get("email")
        message = self.cleaned_data.get("username")
        # print("***********************")
        # print(self.cleaned_data.get("username"))
        # print("***********************")

        if self.cleaned_data.get("username") is None and self.cleaned_data.get("email") is None:
            # raise forms.ValidationError("saldkaslkdnaslkdnalksdn")
            self.add_error("username", "Username is empty\n")
            # self.username.error_messages("hkhbhjbjhbjhbjhbjhbjh")
            self.add_error("email", "Email is empty  ")
            return redirect("/auth/user/add/")


        if self.cleaned_data.get("username") is None:
            # raise forms.ValidationError("saldkaslkdnaslkdnalksdn")
            self.add_error("username", "Username is empty")
            return redirect("/auth/user/add/")

        if self.cleaned_data.get("email") is None:
            # raise forms.ValidationError("saldkaslkdnaslkdnalksdn")
            self.add_error("email", "Email is empty")
            return redirect("/auth/user/add/")
        

        
        # clean_data = self.cleaned_data
        # if clean_data.get("username") == '':
        #     raise forms.ValidationError("Error")
        user=super().save()
        # print("*********" , user.username, "**********")
        # print("****************", user.pk,  "******************")
        # print(self.request)
        # print(self)
        # print( User.objects.get( username = self._meta.model.USERNAME_FIELD))
        uid= urlsafe_base64_encode(force_bytes(user.pk))
        # user: user,
        token= default_token_generator.make_token(user)
        # print("**************", uid, token, "**************")
        domain = "167.172.128.142:8000"
        protocol = "http"
        
        message = render_to_string('webaccount/password_set_user.html', {
            'user':user, 
            'domain':domain,
            'uid': uid,
            'token': token,
            'protocol' : protocol
        })
        email = EmailMessage(mail_subject, message, to=[to_email])
        email.send()
        password = self.cleaned_data.get('password2')
        # if self.cleaned_data.get("username") == "":
        #     forms.ValidationError("sdkfsdknfsdnf")
        if password:
            try:
                password_validation.validate_password(password, self.instance)
            except forms.ValidationError as error:
                self.add_error('password2', error)

    def save(self, commit=True):
        # if self.clean_data.get("username"):
        #     raise forms.ValidationError("aslldknaslkdnaslkd")
        user = super().save(commit=False)
        # print(self.cleaned_data)
        if self.cleaned_data.get("password1"):
            user.set_password(self.cleaned_data["password1"])
        # if self.cleaned_data.get("username") == "":
        #     forms.ValidationError("sdkfsdknfsdnf")
        
        if commit:
            # mail_subject = "Password Set Link"
            # to_email = self.user.email
            # message = "Tetsirt"
            # # print(self.request)
            # # print(self)
            # # print( User.objects.get( username = self._meta.model.USERNAME_FIELD))
            # email = EmailMessage(mail_subject, message, to=[to_email])
            # email.send()
            try:
                user.save()
            except:
                return redirect("/auth/user/add/")
        return user



class UserChangeForm(forms.ModelForm):
    # password = ReadOnlyPasswordHashField(
    #     label=_("Password"),
    #     help_text=_(
    #         "Raw passwords are not stored, so there is no way to see this "
    #         "user's password."
    #     ),
        
    # )

    class Meta:
        model = User
        # fields = '__all__'
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'is_staff', 
            'is_superuser', 
            'is_active'
        ]
        field_classes = {'username': UsernameField}

    def __init__(self,  *args, **kwargs):
        # self.request=request
        # print(self.request)
        super().__init__(*args, **kwargs)
        password = self.fields.get('password')

        # if password:
        #     password.help_text = password.help_text.format('../password/')
        user_permissions = self.fields.get('user_permissions')
        if user_permissions:
            user_permissions.queryset = user_permissions.queryset.select_related('content_type')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial.get('password')

    
    # def _post_clean(self):
    #     mail_subject = "Password Set Link"
    #     to_email = self.cleaned_data.get("email", settings.EMAIL_HOST_USER)
    #     message = "Tetsirt"
    #     # print(self.request)
    #     print(self)
    #     # print( User.objects.get( username = self._meta.model.USERNAME_FIELD))
    #     email = EmailMessage(mail_subject, message, to=[to_email])
    #     email.send()
    #     return super()._post_clean()

    # def save(self, *args, **kwargs):
    #     # do_something()
    #     print("Save")
    #     # super().save(*args, **kwargs)  # Call the "real" save() method.
    #     # do_something_else()
    #     self.uesr.sace

    
#User Can Edit his profile using this Form..........................
class EditProfileForm(UserChangeForm):
    password = forms.CharField(label='', widget = forms.TextInput(attrs = {'type' : 'hidden'}))
    class Meta:
        model = User
        fields = ['username',
                  'first_name',
                  'last_name',
                  'password',
                  'email'
                  ]
