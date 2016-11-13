from django.utils.translation import ugettext_lazy as _
import floppyforms as forms
from misago.forms import Form

class SignInForm(Form):
    user_email = forms.EmailField(max_length=255, label=_("Seu email"))
    user_password = forms.CharField(widget=forms.PasswordInput, max_length=255, label=_("Sua senha"))
    user_remember_me = forms.BooleanField(label=_("Fique conectado"), help_text=_("Lembre de mim"), required=False)

    def __init__(self, *args, **kwargs):
        show_remember_me = kwargs.pop('show_remember_me')

        super(SignInForm, self).__init__(*args, **kwargs)
        if not show_remember_me:
            del self.fields['user_remember_me']
