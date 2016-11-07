from django.conf import settings
from django.core.cache import cache, InvalidCacheBackendError
from django.utils.importlib import import_module
from misago.forms import Form, FormIterator
from misago.models import Forum, ForumRole
from misago.monitor import monitor

class ACLFormBase(Form):
    def iterator(self):
        return FormIterator(self)


def build_form(request, role):
    form_type = type('ACLFormFinal', (ACLFormBase,), {'fieldsets': []})
    for provider in settings.PERMISSION_PROVIDERS:
        app_module = import_module(provider)
        try:
            app_module.make_form(request, role, form_type)
        except AttributeError:
            pass
    return form_type


def build_forum_form(request, role):
    form_type = type('ACLFormForumFinal', (ACLFormBase,), {'fieldsets': []})
    for provider in settings.PERMISSION_PROVIDERS:
        app_module = import_module(provider)
        try:
            app_module.make_forum_form(request, role, form_type)
        except AttributeError as e:
            if not 'make_forum_form' in unicode(e):
                raise e
    return form_type


class BaseACL(object):
    def __init__(self):
        self.acl = {}

    def __repr__(self):
        return '%s (%s)' % (self.__class__.__name__[0:-3],
                            self.__class__.__module__)


class ACL(object):
    def __init__(self, version):
        self.version = version
        self.team = False

    def __iter__(self):
        for attr in dir(self):
            if not attr.startswith("__") and attr not in ['team', 'version']:
                yield self.__dict__[attr]


def acl(user):
    acl_key = user.make_acl_key()
    try:
        user_acl = cache.get(acl_key)
        if user_acl.version != monitor['acl_version']:
            raise InvalidCacheBackendError()
    except (AttributeError, InvalidCacheBackendError):
        user_acl = build_acl(user.get_roles())
        cache.set(acl_key, user_acl, 2592000)
    return user_acl


def build_acl(roles):
    new_acl = ACL(monitor['acl_version'])
    forums = Forum.objects.get(special='root').get_descendants().order_by('lft')
    perms = []
    forum_roles = {}

    for role in roles:
        perms.append(role.permissions)

    for role in ForumRole.objects.all():
        forum_roles[role.pk] = role.permissions

    for provider in settings.PERMISSION_PROVIDERS:
        app_module = import_module(provider)
        try:
            app_module.build(new_acl, perms)
        except AttributeError:
            pass
        try:
            app_module.build_forums(new_acl, perms, forums, forum_roles)
        except AttributeError:
            pass

    for provider in settings.PERMISSION_PROVIDERS:
        app_module = import_module(provider)
        try:
            app_module.cleanup(new_acl, perms, forums)
        except AttributeError:
            pass

    return new_acl
