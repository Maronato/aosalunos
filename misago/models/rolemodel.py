from django.db import models
from django.utils.translation import ugettext as _
import base64
try:
    import cPickle as pickle
except ImportError:
    import pickle

class Role(models.Model):
    """
    Misago User Role model
    """
    name = models.CharField(max_length=255)
    _special = models.CharField(db_column='special', max_length=255,null=True,blank=True)
    protected = models.BooleanField(default=False)
    _permissions = models.TextField(db_column='permissions', null=True, blank=True)
    permissions_cache = {}

    class Meta:
        app_label = 'misago'
    
    def __unicode__(self):
        return unicode(_(self.name))
    
    @property
    def special(self):
        return self._special

    @property
    def permissions(self):
        if self.permissions_cache:
            return self.permissions_cache

        try:
            self.permissions_cache = pickle.loads(base64.decodestring(self._permissions))
        except Exception:
            # ValueError, SuspiciousOperation, unpickling exceptions. If any of
            # these happen, just return an empty dictionary (an empty permissions list).
            self.permissions_cache = {}

        return self.permissions_cache

    @permissions.setter
    def permissions(self, permissions):
        self.permissions_cache = permissions
        self._permissions = base64.encodestring(pickle.dumps(permissions, pickle.HIGHEST_PROTOCOL))