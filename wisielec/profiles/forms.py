# -*- coding: utf-8 -*-
from django import forms
from profiles.models import UserProfile
from django.contrib.auth import authenticate
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import int_to_base36


class ProfileForm(forms.ModelForm):
    password1 = forms.CharField(label=u"Hasło",
                                widget=forms.PasswordInput(render_value=False))
    password2 = forms.CharField(label=u"Potwierdź hasło",
                                widget=forms.PasswordInput(render_value=False))

    class Meta:
        model = UserProfile
        fields = ['username', 'email', ]

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)

        # iterate through fields
        for field in self.fields:
            # set bootstrap classes
            self.fields[field].widget.attrs['class'] = "form-control"

            # password field requires special treatment
            if field.startswith("password"):
                # kill autocomplete
                self.fields[field].widget.attrs["autocomplete"] = "off"
                self.fields[field].widget.attrs.pop("required", "")

                # password field is not required if you're editing it
                if self.instance:
                    self.fields[field].required = False
                    # add helptext to 1st field
                    if field == "password1":
                        self.fields[field].help_text = u"Pozostaw puste jeśli nie zmieniasz hasła"

    def clean_password2(self):
        """
        Ensure the password fields are equal.
        """
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if password1:
            if password1 != password2:
                self._errors["password1"] = self.error_class([u"Podane hasła się nie zgadzają"])
        return password2

    def clean_email(self):
        """
        Ensure the email address is not already registered.
        """
        email = self.cleaned_data.get("email")
        qs = UserProfile.objects.exclude(id=self.instance.id).filter(email=email)
        if len(qs) == 0:
            return email
        raise forms.ValidationError("This email is already registered")

    def save(self, *args, **kwargs):
        # verify form first
        kwargs["commit"] = False
        user = super(ProfileForm, self).save(*args, **kwargs)

        # get password
        password = self.cleaned_data.get("password1")
        if password:
            # attempt to set password
            user.set_password(password)
        elif not self.instance:
            try:
                user.set_unusable_password()
            except AttributeError:
                # This could happen if using a custom user model that
                # doesn't inherit from Django's AbstractBaseUser.
                pass

        # actually save form
        user.save()

        return user
