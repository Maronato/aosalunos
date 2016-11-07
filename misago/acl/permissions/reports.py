from django.utils.translation import ugettext_lazy as _
import floppyforms as forms
from misago.acl.builder import BaseACL
from misago.acl.exceptions import ACLError403, ACLError404
from misago.forms import YesNoSwitch
from misago.models import Forum

def make_form(request, role, form):
    if role.special != 'guest':
        form.base_fields['can_report_content'] = forms.BooleanField(label=_("Can report content"),
                                                                    widget=YesNoSwitch, initial=False, required=False)
        form.base_fields['can_handle_reports'] = forms.BooleanField(label=_("Can handle reports"),
                                                                    widget=YesNoSwitch, initial=False, required=False)
        form.base_fields['can_upload_report_attachments'] = forms.BooleanField(label=_("Can upload attachments in reports discussions"),
                                                                               widget=YesNoSwitch, initial=False, required=False)
        form.base_fields['can_download_report_attachments'] = forms.BooleanField(label=_("Can download attachments in reports discussions"),
                                                                                 widget=YesNoSwitch, initial=False, required=False)
        form.base_fields['report_attachment_size'] = forms.IntegerField(label=_("Max size of single attachment in reports discussions (in Kb)"),
                                                                        help_text=_("Enter zero for no limit."),
                                                                        min_value=0, initial=100)
        form.base_fields['report_attachment_limit'] = forms.IntegerField(label=_("Max number of attachments per post in reports discussions"),
                                                                         help_text=_("Enter zero for no limit."),
                                                                         min_value=0, initial=3)
        form.base_fields['can_mod_reports_discussions'] = forms.BooleanField(label=_("Can moderate reports discussions"),
                                                                             widget=YesNoSwitch, initial=False, required=False)
        form.base_fields['can_delete_reports'] = forms.TypedChoiceField(label=_("Can delete reports"),
                                                                        choices=(
                                                                                  (0, _("No")),
                                                                                  (1, _("Yes, soft-delete")),
                                                                                  (2, _("Yes, hard-delete")),
                                                                                 ), coerce=int)

        form.fieldsets.append((
                               _("Reporting Content"),
                               ('can_report_content', 'can_handle_reports',
                                'can_upload_report_attachments', 'can_download_report_attachments',
                                'report_attachment_size', 'report_attachment_limit',
                                'can_mod_reports_discussions', 'can_delete_reports')
                              ))


class ReportsACL(BaseACL):
    def can_report(self):
        return self.acl['can_report_content']

    def allow_report(self):
        if not self.acl['can_report_content']:
            raise ACLError403(_("You don't have permission to report posts."))

    def can_handle(self):
        return self.acl['can_handle_reports']

    def is_mod(self):
        return self.acl['can_mod_reports_discussions']

    def can_delete(self):
        return self.acl['can_delete_reports']


def build(acl, roles):
    acl.reports = ReportsACL()
    acl.reports.acl['can_report_content'] = False
    acl.reports.acl['can_handle_reports'] = False
    acl.reports.acl['can_upload_report_attachments'] = True
    acl.reports.acl['can_download_report_attachments'] = True
    acl.reports.acl['report_attachment_size'] = 300
    acl.reports.acl['report_attachment_limit'] = 6
    acl.reports.acl['can_mod_reports_discussions'] = False
    acl.reports.acl['can_delete_reports'] = False

    for role in roles:
        for perm, value in acl.reports.acl.items():
            if perm in role and role[perm] > value:
                acl.reports.acl[perm] = role[perm]


def cleanup(acl, perms, forums):
    forum = Forum.objects.special_pk('reports')
    acl.threads.acl[forum] = {
                              'can_read_threads': 2,
                              'can_start_threads': 0,
                              'can_edit_own_threads': True,
                              'can_soft_delete_own_threads': False,
                              'can_write_posts': 2,
                              'can_edit_own_posts': True,
                              'can_soft_delete_own_posts': True,
                              'can_upvote_posts': False,
                              'can_downvote_posts': False,
                              'can_see_posts_scores': 0,
                              'can_see_votes': False,
                              'can_make_polls': False,
                              'can_vote_in_polls': False,
                              'can_see_poll_votes': False,
                              'can_upload_attachments': False,
                              'can_download_attachments': False,
                              'attachment_size': 100,
                              'attachment_limit': 3,
                              'can_approve': False,
                              'can_edit_labels': False,
                              'can_see_changelog': True,
                              'can_pin_threads': 0,
                              'can_edit_threads_posts': False,
                              'can_move_threads_posts': False,
                              'can_close_threads': False,
                              'can_protect_posts': False,
                              'can_delete_threads': 0,
                              'can_delete_posts': 0,
                              'can_delete_polls': 0,
                              'can_delete_attachments': False,
                              'can_delete_checkpoints': 0,
                              'can_see_deleted_checkpoints': False,
                             }

    for perm in perms:
        try:
            if perm['can_handle_reports'] and forum not in acl.forums.acl['can_see']:
                acl.forums.acl['can_see'].append(forum)
                acl.forums.acl['can_browse'].append(forum)
                acl.threads.acl[forum]['can_pin_threads'] = 2
            if perm['can_upload_report_attachments']:
                acl.threads.acl[forum]['can_upload_attachments'] = True
            if perm['can_download_report_attachments']:
                acl.threads.acl[forum]['can_download_attachments'] = True
            if (perm['report_attachment_size'] > acl.threads.acl[forum]['attachment_size']
                    and acl.threads.acl[forum]['attachment_size'] != 0):
                acl.threads.acl[forum]['attachment_size'] = perm['report_attachment_size']
            if (perm['report_attachment_limit'] > acl.threads.acl[forum]['attachment_limit']
                    and acl.threads.acl[forum]['attachment_limit'] != 0):
                acl.threads.acl[forum]['attachment_limit'] = perm['report_attachment_limit']
            if perm['can_mod_reports_discussions']:
                acl.threads.acl[forum]['can_edit_threads_posts'] = True
                acl.threads.acl[forum]['can_delete_posts'] = 2
                acl.threads.acl[forum]['can_delete_attachments'] = True
                acl.threads.acl[forum]['can_delete_checkpoints'] = 2
                acl.threads.acl[forum]['can_see_deleted_checkpoints'] = True
            if perm['can_delete_reports'] > acl.threads.acl[forum]['can_delete_threads']:
                acl.threads.acl[forum]['can_delete_threads'] = perm['can_delete_reports']
        except KeyError:
            pass
