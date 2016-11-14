
# -*- coding: UTF-8 -*-
from django import forms
from misago.models import User
import re


class DACInfo(forms.Form):
    username = forms.CharField(label=u"Nome de usuário para o fórum",
                               max_length=16,
                               min_length=3,
                               required=True,
                               widget=forms.TextInput(attrs={'class': "form-control"}),
                               )

    # matricula = forms.CharField(label=u"Código de Matrícula",
    #                            max_length=200,
    #                            required=True,
    #                            widget=forms.TextInput(attrs={'class': "form-control"}),
    #                            )

    email = forms.EmailField(label=u"Email da DAC (usado para fazer login)",
                                widget=forms.EmailInput(attrs={'class': "form-control", 'placeholder': "a111111@dac.unicamp.br"}),
                                required=True,
                               )

    password1 = forms.CharField(label=u"Senha",
                                widget=forms.PasswordInput(attrs={'class': "form-control"}),
                                required=True,
                                max_length=30,
                                min_length=4,
                               )

    password2 = forms.CharField(label=u"Confirme a senha",
                                widget=forms.PasswordInput(attrs={'class': "form-control"}),
                                required=True,
                                max_length=20,
                                min_length=4,
                               )

    def clean(self):
        cleaned_data = super(DACInfo, self).clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")
        email = cleaned_data.get("email")
        username = cleaned_data.get("username")

        if username:
            if not username.isalnum():
                raise forms.ValidationError(
                    "Usuário só pode conter letras e números!"
                )


        if password1 != password2:
            raise forms.ValidationError(
                "Senhas diferentes!"
            )

        if email:
            if not re.match(r'^[a-z]\d+@dac.unicamp.br$', email, re.I):
                raise forms.ValidationError(
                    "Email não é da DAC!"
                )
            else:
                cleaned_data["ra"] = int(re.findall(r'[a-z](\d+)@', email, re.I)[0])

        # if cleaned_data.get("matricula"):
        #     error, value = core.check_code(cleaned_data.get("matricula"))
        #     if error != 1:
        #         raise forms.ValidationError(
        #             value
        #         )
        #         return cleaned_data

        #     ra = core.check_fields(value)['ra']
        #     cleaned_data["ra"] = ra
        #     profile = Profile.user_from_ra(ra)
        #     if profile is not None:
        #         raise forms.ValidationError(
        #             "RA já cadastrado!"
        #         )

        if len(User.objects.filter(username=cleaned_data.get("username"))) != 0:
            raise forms.ValidationError(
                "Nome de usuário já cadastrado!"
            )

        if len(User.objects.filter(email=cleaned_data.get("email"))) != 0:
            raise forms.ValidationError(
                "Email já cadastrado!"
            )

        return cleaned_data
