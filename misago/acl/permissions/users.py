from django.utils.translation import ugettext_lazy as _
import floppyforms as forms
from misago.acl.builder import BaseACL
from misago.acl.exceptions import ACLError404
from misago.forms import YesNoSwitch

def make_form(request, role, form):
    form.base_fields['can_search_users'] = forms.BooleanField(label=_("Can search user profiles"),
                                                              widget=YesNoSwitch, initial=False, required=False)
    form.base_fields['can_see_users_emails'] = forms.BooleanField(label=_("Can see members e-mail's"),
                                                                  widget=YesNoSwitch, initial=False, required=False)
    form.base_fields['can_see_users_trails'] = forms.BooleanField(label=_("Can see members ip's and user-agents"),
                                                                  widget=YesNoSwitch, initial=False, required=False)
    form.base_fields['can_see_hidden_users'] = forms.BooleanField(label=_("Can see mebers that hide their presence"),
                                                                  widget=YesNoSwitch, initial=False, required=False)

    form.fieldsets.append((
                           _("User Profiles"),
                           ('can_search_users', 'can_see_users_emails', 'can_see_users_trails', 'can_see_hidden_users')
                          ))


class UsersACL(BaseACL):
    def can_search_users(self):
        return self.acl['can_search_users']

    def can_see_users_emails(self):
        return self.acl['can_see_users_emails']

    def can_see_users_trails(self):
        return self.acl['can_see_users_trails']

    def can_see_hidden_users(self):
        return self.acl['can_see_hidden_users']

    def allow_details_view(self):
        if not self.acl['can_see_users_trails']:
            raise ACLError404()


def build(acl, roles):
    acl.users = UsersACL()
    acl.users.acl['can_search_users'] = False
    acl.users.acl['can_see_users_emails'] = False
    acl.users.acl['can_see_users_trails'] = False
    acl.users.acl['can_see_hidden_users'] = False

    for role in roles:
        try:
            if 'can_search_users' in role and role['can_search_users']:
                acl.users.acl['can_search_users'] = True

            if 'can_see_users_emails' in role and role['can_see_users_emails']:
                acl.users.acl['can_see_users_emails'] = True

            if 'can_see_users_trails' in role and role['can_see_users_trails']:
                acl.users.acl['can_see_users_trails'] = True

            if 'can_see_hidden_users' in role and role['can_see_hidden_users']:
                acl.users.acl['can_see_hidden_users'] = True
        except KeyError:
            pass
