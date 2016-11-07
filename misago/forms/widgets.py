from recaptcha.client.captcha import displayhtml
import floppyforms as forms
from misago.conf import settings

class ReCaptchaWidget(forms.TextInput):
    def render(self):
        return displayhtml(settings.recaptcha_public,
                           settings.recaptcha_ssl)


class YesNoSwitch(forms.CheckboxInput):
    pass


class ForumTOS(forms.CheckboxInput):
    pass
