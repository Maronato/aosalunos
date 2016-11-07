from misago.utils.fixtures import load_settings_fixture, update_settings_fixture
from misago.utils.translation import ugettext_lazy as _

settings_fixture = (
    # Avatars Settings
    ('tos', {
         'name': _("Forum Terms of Service"),
         'description': _("Those settings allow you to set up forum terms of service."),
         'settings': (
            ('tos_title', {
                'value':        "Terms of Service",
                'type':         "string",
                'input':        "text",
                'separator':    _("Terms of Service Options"),
                'name':         _("Page Title"),
                'description':  _("Title of page community ToS are displayed on."),
            }),
            ('tos_url', {
                'value':        "",
                'type':         "string",
                'input':        "text",
                'name':         _("Link to remote page with ToS"),
                'description':  _("If your forum's ToS are located on remote page, enter here its address."),
            }),
            ('tos_content', {
                'value':        "",
                'type':         "string",
                'input':        "textarea",
                'name':         _("OR enter ToS content"),
                'description':  _("Instead of linking to remote page, forum can create dedicated ToS page for you. To display ToS page, enter here your forum Terms of Service."),
            }),
       ),
    }),
)


def load():
    load_settings_fixture(settings_fixture)


def update():
    update_settings_fixture(settings_fixture)
