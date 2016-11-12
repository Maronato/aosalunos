
# -*- coding: UTF-8 -*-
from django import forms
from .models import Members


class AddPromise(forms.Form):
    title = forms.CharField(label=u"Título da Proposta",
                               max_length=200,
                               required=True,
                               widget=forms.TextInput(attrs={'class': "form-control"}),
                               )

    text = forms.CharField(label=u"Texto da proposta",
                                widget=forms.Textarea(attrs={'class': "form-control"}),
                                required=True,
                               )


class EditProfile(forms.ModelForm):
    class Meta:
        model = Members
        fields = ['picture', 'name', 'role', 'occupation', 'description', 'facebook', 'twitter', 'github', 'email']
        widgets = {
            'picture': forms.TextInput(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'role': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.TextInput(attrs={'class': 'form-control'}),
            'occupation': forms.TextInput(attrs={'class': 'form-control'}),
            'facebook': forms.TextInput(attrs={'class': 'form-control'}),
            'twitter': forms.TextInput(attrs={'class': 'form-control'}),
            'github': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'picture': 'URL de foto de Perfil (Use uma foto quadrada)',
            'name': 'Seu nome',
            'role': u'Na chapa eu sou...',
            'occupation': u'Na vida eu sou...',
            'description': u'Uma breve descrição sua',
            'facebook': 'URL do seu Facebook',
            'twitter': 'URL do seu Twitter',
            'github': 'URL do seu GitHub',
            'email': 'Um email pra contato'
        }
