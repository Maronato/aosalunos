import copy
from django.db import models
from django.db.models import F
from django.db.models.signals import pre_save, pre_delete
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from misago.markdown import clear_markdown
from misago.signals import (delete_user_content, merge_post, merge_thread,
                            move_forum_content, move_post, move_thread,
                            rename_user, sync_user_profile)
from misago.utils.translation import ugettext_lazy
import base64
try:
    import cPickle as pickle
except ImportError:
    import pickle

class PostManager(models.Manager):
    def filter_stats(self, start, end):
        return self.filter(date__gte=start).filter(date__lte=end)


class Post(models.Model):
    forum = models.ForeignKey('Forum')
    thread = models.ForeignKey('Thread')
    user = models.ForeignKey('User', null=True, blank=True, on_delete=models.SET_NULL)
    user_name = models.CharField(max_length=255)
    ip = models.GenericIPAddressField()
    agent = models.CharField(max_length=255)
    post = models.TextField()
    post_preparsed = models.TextField()
    upvotes = models.PositiveIntegerField(default=0)
    downvotes = models.PositiveIntegerField(default=0)
    mentions = models.ManyToManyField('User', related_name="mention_set")
    date = models.DateTimeField()
    current_date = models.DateTimeField(db_index=True)
    edits = models.PositiveIntegerField(default=0)
    edit_reason = models.CharField(max_length=255, null=True, blank=True)
    edit_user = models.ForeignKey('User', related_name='+', null=True, blank=True, on_delete=models.SET_NULL)
    edit_user_name = models.CharField(max_length=255, null=True, blank=True)
    edit_user_slug = models.SlugField(max_length=255, null=True, blank=True)
    delete_date = models.DateTimeField(null=True, blank=True)
    reported = models.BooleanField(default=False, db_index=True)
    reports = models.CharField(max_length=255, null=True, blank=True)
    moderated = models.BooleanField(default=False)
    deleted = models.BooleanField(default=False)
    protected = models.BooleanField(default=False)
    has_attachments = models.BooleanField(default=False)
    _attachments = models.TextField(db_column='attachments', null=True, blank=True)

    objects = PostManager()

    statistics_name = _('New Posts')

    class Meta:
        app_label = 'misago'

    @property
    def attachments(self):
        if not self.has_attachments:
            return []

        try:
            return self._attachments_cache
        except AttributeError:
            pass

        try:
            self._attachments_cache = pickle.loads(base64.decodestring(self._attachments))
        except Exception:
            self._attachments_cache = []
        return self._attachments_cache


    @attachments.setter
    def attachments(self, new_attachments):
        if new_attachments:
            self._update_attachments_store(new_attachments)
        else:
            self._empty_attachments_store()

    def _empty_attachments_store(self):
        self.has_attachments = False
        self._attachments = None

    def _update_attachments_store(self, new_attachments):
        self.has_attachments = True
        clean_attachments = []
        for attachment in new_attachments:
            attachment = copy.copy(attachment)
            attachment_user_pk = attachment.user_id
            attachment.user = None
            attachment.user_id = attachment_user_pk
            attachment.forum = None
            attachment.thread = None
            attachment.post = None

            clean_attachments.append(attachment)
        self._attachments = base64.encodestring(pickle.dumps(clean_attachments, pickle.HIGHEST_PROTOCOL))

    def sync_attachments(self):
        if self.attachment_set.exists():
            self.attachments = self.attachment_set.iterator()
        else:
            self._empty_attachments_store()

    @property
    def timeline_date(self):
        return self.date

    def save(self, *args, **kwargs):
        self.current_date = timezone.now()
        return super(Post, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        """
        FUGLY HAX for weird stuff that happens with
        relations on model deletion in MySQL
        """
        if self.reported:
            self.report_set.update(report_for=None)
        return super(Post, self).delete(*args, **kwargs)

    def get_date(self):
        return self.date

    def quote(self):
        quote = []
        quote.append('@%s' % self.user_name)
        for line in self.post.splitlines():
            quote.append('> %s' % line)
        quote.append('\r\n')
        return '\r\n'.join(quote)

    @property
    def post_clean(self):
        return clear_markdown(self.post_preparsed)

    def move_to(self, thread):
        move_post.send(sender=self, move_to=thread)
        self.thread = thread
        self.forum = thread.forum

    def merge_with(self, post):
        post.post = '%s\n- - -\n%s' % (post.post, self.post)
        merge_post.send(sender=self, new_post=post)

    def notify_mentioned(self, request, thread_type, users):
        from misago.acl.exceptions import ACLError403, ACLError404

        mentioned = self.mentions.all()
        for slug, user in users.items():
            if user.pk != request.user.pk and user not in mentioned:
                self.mentions.add(user)
                try:
                    user_acl = user.acl()
                    user_acl.forums.allow_forum_view(self.forum)
                    user_acl.threads.allow_thread_view(user, self.thread)
                    user_acl.threads.allow_post_view(user, self.thread, self)
                    if not user.is_ignoring(request.user):
                        alert = user.alert(ugettext_lazy("%(username)s has mentioned you in his reply in thread %(thread)s").message)
                        alert.profile('username', request.user)
                        alert.post('thread', thread_type, self.thread, self)
                        alert.save_all()
                except (ACLError403, ACLError404):
                    pass

    def is_reported(self):
        self.reported = self.report_set.filter(weight=2).count() > 0

    def live_report(self):
        try:
            return self.report_set.filter(weight=2)[0]
        except IndexError:
            return None

    def add_reporter(self, user):
        if not self.reports:
            self.reports = ','
        self.reports += '%s,' % user.pk

    def reported_by(self, user):
        if not self.reports:
            return False
        try:
            return ',%s,' % user.pk in self.reports
        except AttributeError:
            return ',%s,' % user in self.reports


def rename_user_handler(sender, **kwargs):
    Post.objects.filter(user=sender).update(
                                            user_name=sender.username,
                                            current_date=timezone.now(),
                                            )
    Post.objects.filter(edit_user=sender).update(
                                                 edit_user_name=sender.username,
                                                 edit_user_slug=sender.username_slug,
                                                 )

rename_user.connect(rename_user_handler, dispatch_uid="rename_user_posts")


def delete_user_content_handler(sender, **kwargs):
    from misago.models import Thread

    threads = []
    for post in sender.post_set.distinct().values('thread_id').iterator():
        if not post['thread_id'] in threads:
            threads.append(post['thread_id'])

    sender.post_set.all().delete()

    for thread in Thread.objects.filter(id__in=threads).iterator():
        thread.sync()
        thread.save(force_update=True)

delete_user_content.connect(delete_user_content_handler, dispatch_uid="delete_user_posts")


def move_forum_content_handler(sender, **kwargs):
    Post.objects.filter(forum=sender).update(forum=kwargs['move_to'])

move_forum_content.connect(move_forum_content_handler, dispatch_uid="move_forum_posts")


def move_thread_handler(sender, **kwargs):
    Post.objects.filter(thread=sender).update(forum=kwargs['move_to'])

move_thread.connect(move_thread_handler, dispatch_uid="move_thread_posts")


def merge_thread_handler(sender, **kwargs):
    Post.objects.filter(thread=sender).update(thread=kwargs['new_thread'])

merge_thread.connect(merge_thread_handler, dispatch_uid="merge_threads_posts")


def sync_user_handler(sender, **kwargs):
    sender.posts = sender.post_set.count()

sync_user_profile.connect(sync_user_handler, dispatch_uid="sync_user_posts")
