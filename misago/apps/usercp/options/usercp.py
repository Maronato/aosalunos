from django.utils.translation import ugettext_lazy as _

def register_usercp_extension(request):
    return (('usercp_options', _('Forum Options')),)
