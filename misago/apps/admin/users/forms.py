from PIL import Image
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
import floppyforms as forms
from misago.conf import settings
from misago.forms import Form, YesNoSwitch
from misago.models import Rank, Role, User
from misago.validators import validate_username, validate_password, validate_email

class UserForm(Form):
    username = forms.CharField(label=_("Username"),
                               help_text=_("Username is name under which user is known to other users. Between 3 and 15 characters, only letters and digits are allowed."),
                               max_length=255)
    title = forms.CharField(label=_("User Title"),
                            help_text=_("To override user title with custom one, enter it here."),
                            max_length=255, required=False)
    rank = forms.ModelChoiceField(label=_("User Rank"),
                                  help_text=_("This user rank."),
                                  queryset=Rank.objects.order_by('order').all(), required=False, empty_label=_('No rank assigned'))
    roles = False
    email = forms.EmailField(label=_("E-mail Address"),
                             help_text=_("Member e-mail address."),
                             max_length=255)
    new_password = forms.CharField(label=_("Change User Password"),
                                   help_text=_("If you wish to change user password, enter here new password. Otherwhise leave this field blank."),
                                   max_length=255, required=False, widget=forms.PasswordInput)
    avatar_custom = forms.CharField(label=_("Set Non-Standard Avatar"),
                                    help_text=_("You can make this member use special avatar by entering name of image file located in avatars directory here."),
                                    max_length=255, required=False)
    avatar_ban = forms.BooleanField(label=_("Lock Member's Avatar"),
                                    help_text=_("If you set this field to yes, this member's avatar will be deleted and replaced with random one selected from _removed gallery and member will not be able to change his avatar."),
                                    widget=YesNoSwitch, required=False)
    avatar_ban_reason_user = forms.CharField(label=_("User-visible reason for lock"),
                                             help_text=_("You can leave message to member explaining why he or she is unable to change his avatar anymore. This message will be displayed to member in his control panel."),
                                             widget=forms.Textarea, required=False)
    avatar_ban_reason_admin = forms.CharField(label=_("Forum Team-visible reason for lock"),
                                              help_text=_("You can leave message to other forum team members exmplaining why this member's avatar has been locked."),
                                              widget=forms.Textarea, required=False)
    signature = forms.CharField(label=_("Signature"),
                                help_text=_("Signature is short message attached at end of member's messages."),
                                widget=forms.Textarea, required=False)
    signature_ban = forms.BooleanField(label=_("Lock Member's Signature"),
                                       help_text=_("If you set this field to yes, this member will not be able to change his signature."),
                                       widget=YesNoSwitch, required=False)
    signature_ban_reason_user = forms.CharField(label=_("User-visible reason for lock"),
                                                help_text=_("You can leave message to member explaining why he or she is unable to edit his signature anymore. This message will be displayed to member in his control panel."),
                                                widget=forms.Textarea, required=False)
    signature_ban_reason_admin = forms.CharField(label=_("Forum Team-visible reason for lock"),
                                                 help_text=_("You can leave message to other forum team members exmplaining why this member's signature has been locked."),
                                                 widget=forms.Textarea, required=False)

    def __init__(self, user=None, *args, **kwargs):
        self.request = kwargs['request']
        self.user = user
        super(UserForm, self).__init__(*args, **kwargs)

    def finalize_form(self):
        # Roles list
        if self.request.user.is_god():
            self.add_field('roles', forms.ModelMultipleChoiceField(label=_("User Roles"),
                                                                   help_text=_("This user roles. Roles are sets of user permissions"),
                                                                   widget=forms.CheckboxSelectMultiple, queryset=Role.objects.order_by('name').all(), error_messages={'required': _("User must have at least one role assigned.")}))
        else:
            self.add_field('roles', forms.ModelMultipleChoiceField(label=_("User Roles"),
                                                                   help_text=_("This user roles. Roles are sets of user permissions"),
                                                                   widget=forms.CheckboxSelectMultiple, queryset=Role.objects.filter(protected__exact=False).order_by('name').all(), required=False))

        # Keep non-gods from editing protected members sign-in credentials
        if self.user.is_protected() and not self.request.user.is_god() and self.user.pk != self.request.user.pk:
            del self.fields['email']
            del self.fields['new_password']

    def clean_username(self):
        org_username = self.user.username
        validate_username(self.cleaned_data['username'])
        self.user.set_username(self.cleaned_data['username'])
        try:
            self.user.full_clean()
        except ValidationError as e:
            self.user.is_username_valid(e)
            self.user.set_username(org_username)
        return self.cleaned_data['username']

    def clean_email(self):
        self.user.set_email(self.cleaned_data['email'])
        try:
            self.user.full_clean()
        except ValidationError as e:
            self.user.is_email_valid(e)
        return self.cleaned_data['email']

    def clean_new_password(self):
        if self.cleaned_data['new_password']:
            validate_password(self.cleaned_data['new_password'])
            self.user.set_password(self.cleaned_data['new_password'])
            try:
                self.user.full_clean()
            except ValidationError as e:
                self.user.is_password_valid(e)
            return self.cleaned_data['new_password']
        return ''

    def clean_avatar_custom(self):
        if self.cleaned_data['avatar_custom']:
            try:
                avatar_image = Image.open('%s/avatars/%s' % (settings.STATICFILES_DIRS[0], self.cleaned_data['avatar_custom']))
            except IOError:
                raise ValidationError(_("Avatar does not exist or is not image file."))
            return self.cleaned_data['avatar_custom']
        return ''


class NewUserForm(Form):
    username = forms.CharField(label=_("Username"),
                               help_text=_("Username is name under which user is known to other users. Between 3 and 15 characters, only letters and digits are allowed."),
                               max_length=255)
    title = forms.CharField(label=_("User Title"),
                            help_text=_("To override user title with custom one, enter it here."),
                            max_length=255, required=False)
    rank = forms.ModelChoiceField(label=_("User Rank"),
                                  help_text=_("This user rank."),
                                  queryset=Rank.objects.order_by('order').all(), required=False, empty_label=_('No rank assigned'))
    roles = False
    email = forms.EmailField(label=_("E-mail Address"),
                             help_text=_("Member e-mail address."),
                             max_length=255)
    password = forms.CharField(label=_("User Password"),
                               help_text=_("Member password."),
                               max_length=255, widget=forms.PasswordInput)

    def finalize_form(self):
        if self.request.user.is_god():
            self.add_field('roles', forms.ModelMultipleChoiceField(label=_("User Roles"),
                                                                   help_text=_("This user roles. Roles are sets of user permissions"),
                                                                   widget=forms.CheckboxSelectMultiple, queryset=Role.objects.order_by('name').all(), error_messages={'required': _("User must have at least one role assigned.")}))
        else:
            self.add_field('roles', forms.ModelMultipleChoiceField(label=_("User Roles"),
                                                                   help_text=_("This user roles. Roles are sets of user permissions"),
                                                                   widget=forms.CheckboxSelectMultiple, queryset=Role.objects.filter(protected__exact=False).order_by('name').all(), required=False))

    def clean_username(self):
        validate_username(self.cleaned_data['username'])
        new_user = User.objects.get_blank_user()
        new_user.set_username(self.cleaned_data['username'])
        try:
            new_user.full_clean()
        except ValidationError as e:
            new_user.is_username_valid(e)
        return self.cleaned_data['username']

    def clean_email(self):
        new_user = User.objects.get_blank_user()
        new_user.set_email(self.cleaned_data['email'])
        try:
            new_user.full_clean()
        except ValidationError as e:
            new_user.is_email_valid(e)
        return self.cleaned_data['email']

    def clean_password(self):
        new_user = User.objects.get_blank_user()
        new_user.set_password(self.cleaned_data['password'])
        try:
            new_user.full_clean()
        except ValidationError as e:
            new_user.is_password_valid(e)
        validate_password(self.cleaned_data['password'])
        return self.cleaned_data['password']


class SearchUsersForm(Form):
    username = forms.CharField(label=_("Username"), max_length=255, required=False)
    email = forms.CharField(label=_("E-mail Address"), max_length=255, required=False)
    activation = forms.TypedMultipleChoiceField(label=_("Activation Requirement"), widget=forms.CheckboxSelectMultiple, choices=((0, _("Already Active")), (1, _("By User")), (2, _("By Administrator"))), coerce=int, required=False)
    rank = forms.ModelMultipleChoiceField(label=_("Rank is"), widget=forms.CheckboxSelectMultiple, queryset=Rank.objects.order_by('order').all(), required=False)
    role = forms.ModelMultipleChoiceField(label=_("Has Role"), widget=forms.CheckboxSelectMultiple, queryset=Role.objects.order_by('name').all(), required=False)