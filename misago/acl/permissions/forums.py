from django.utils.translation import ugettext_lazy as _
import floppyforms as forms
from misago.acl.builder import BaseACL
from misago.acl.exceptions import ACLError403, ACLError404
from misago.forms import YesNoSwitch

def make_forum_form(request, role, form):
    form.base_fields['can_see_forum'] = forms.BooleanField(label=_("Can see forum"),
                                                           widget=YesNoSwitch, initial=False, required=False)
    form.base_fields['can_see_forum_contents'] = forms.BooleanField(label=_("Can see forum contents"),
                                                                    widget=YesNoSwitch, initial=False, required=False)
    form.fieldsets.append((
                           _("Forums Permissions"),
                           ('can_see_forum', 'can_see_forum_contents'),
                          ))


class ForumsACL(BaseACL):
    def known_forums(self):
        return self.acl['can_see']

    def can_see(self, forum):
        try:
            return forum.pk in self.acl['can_see']
        except AttributeError:
            return long(forum) in self.acl['can_see']

    def can_browse(self, forum):
        if self.can_see(forum):
            try:
                return forum.pk in self.acl['can_browse']
            except AttributeError:
                return long(forum) in self.acl['can_browse']
        return False

    def allow_forum_view(self, forum):
        if not self.can_see(forum):
            raise ACLError404()
        if not self.can_browse(forum):
            raise ACLError403(_("You don't have permission to browse this forum."))


def build_forums(acl, perms, forums, forum_roles):
    acl.forums = ForumsACL()
    acl.forums.acl['can_see'] = []
    acl.forums.acl['can_browse'] = []

    for forum in forums:
        for perm in perms:
            try:
                role = forum_roles[perm['forums'][forum.pk]]
                if role['can_see_forum'] and forum.pk not in acl.forums.acl['can_see']:
                    acl.forums.acl['can_see'].append(forum.pk)
                if role['can_see_forum_contents'] and forum.pk not in acl.forums.acl['can_browse']:
                    acl.forums.acl['can_browse'].append(forum.pk)
            except KeyError:
                pass


def cleanup(acl, perms, forums):
    for forum in forums:
        if forum.pk in acl.forums.acl['can_browse'] and not forum.pk in acl.forums.acl['can_see']:
            # First burp: we can read forum but we cant see forum
            del acl.forums.acl['can_browse'][acl.forums.acl['can_browse'].index(forum.pk)]

        if forum.level > 1:
            if forum.parent_id not in acl.forums.acl['can_see'] or forum.parent_id not in acl.forums.acl['can_browse']:
                # Second burp: we cant see or read parent forum
                try:
                    del acl.forums.acl['can_see'][acl.forums.acl['can_see'].index(forum.pk)]
                except ValueError:
                    pass
                try:
                    del acl.forums.acl['can_browse'][acl.forums.acl['can_browse'].index(forum.pk)]
                except ValueError:
                    pass
