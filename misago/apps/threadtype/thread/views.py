from django.core.urlresolvers import reverse
from django.forms import ValidationError
from django.http import Http404
from django.shortcuts import redirect
from django.template import RequestContext
from django.utils import timezone
from django.utils.translation import ugettext as _
import floppyforms as forms
from misago import messages
from misago.acl.exceptions import ACLError403, ACLError404
from misago.apps.errors import error403, error404
from misago.conf import settings
from misago.forms import Form
from misago.markdown import emojis
from misago.messages import Message
from misago.models import Forum, Thread, Post, Karma, WatchedThread
from misago.readstrackers import ThreadsTracker
from misago.shortcuts import render_to_response
from misago.utils.pagination import make_pagination
from misago.apps.threadtype.base import ViewBase
from misago.apps.threadtype.thread.forms import QuickReplyForm

class ThreadBaseView(ViewBase):
    def fetch_thread(self):
        self.thread = Thread.objects.get(pk=self.kwargs.get('thread'))
        self.forum = self.thread.forum
        self.proxy = Forum.objects.parents_aware_forum(self.forum)
        self.request.acl.forums.allow_forum_view(self.forum)
        self.request.acl.threads.allow_thread_view(self.request.user, self.thread)

        if self.forum.level:
            self.parents = Forum.objects.forum_parents(self.forum.pk, True)

        self.tracker = ThreadsTracker(self.request, self.forum)
        if self.request.user.is_authenticated():
            try:
                self.watcher = WatchedThread.objects.get(user=self.request.user, thread=self.thread)
            except WatchedThread.DoesNotExist:
                pass

    def fetch_posts(self):
        self.count = self.request.acl.threads.filter_posts(self.request, self.thread, Post.objects.filter(thread=self.thread)).count()
        self.posts = self.request.acl.threads.filter_posts(self.request, self.thread, Post.objects.filter(thread=self.thread)).prefetch_related('user', 'user__rank')

        self.posts = self.posts.order_by('id')

        try:
            self.pagination = make_pagination(self.kwargs.get('page', 0), self.count, settings.posts_per_page)
        except Http404:
            return redirect(reverse(self.type_prefix, kwargs={'thread': self.thread.pk, 'slug': self.thread.slug}))

        checkpoints_boundary = None

        if self.pagination['total'] > 1:
            self.posts = self.posts[self.pagination['start']:self.pagination['stop'] + 1]
            posts_len = len(self.posts)
            if self.pagination['page'] < self.pagination['total']:
                checkpoints_boundary = self.posts[posts_len - 1].date
                self.posts = self.posts[0:(posts_len - 1)]

        self.read_date = self.tracker.read_date(self.thread)

        ignored_users = []
        if self.request.user.is_authenticated():
            ignored_users = self.request.user.ignored_users()

        posts_dict = {}
        for post in self.posts:
            posts_dict[post.pk] = post
            post.message = self.request.messages.get_message('threads_%s' % post.pk)
            post.is_read = post.date <= self.read_date or (post.pk != self.thread.start_post_id and post.moderated)
            post.karma_vote = None
            post.ignored = self.thread.start_post_id != post.pk and not self.thread.pk in self.request.session.get('unignore_threads', []) and post.user_id in ignored_users
            if post.ignored:
                self.ignored = True

        self.thread.add_checkpoints_to_posts(self.request.acl.threads.can_see_all_checkpoints(self.forum),
                                             self.posts,
                                             (self.posts[0].date if self.pagination['page'] > 1 else None),
                                             checkpoints_boundary)

        last_post = self.posts[len(self.posts) - 1]

        if not self.tracker.is_read(self.thread):
            self.tracker_update(last_post)

        if self.watcher and last_post.date > self.watcher.last_read:
            self.watcher.last_read = timezone.now()
            self.watcher.save(force_update=True)

        if self.request.user.is_authenticated():
            for karma in Karma.objects.filter(post_id__in=posts_dict.keys()).filter(user=self.request.user):
                posts_dict[karma.post_id].karma_vote = karma

    def tracker_update(self, last_post):
        self.tracker.set_read(self.thread, last_post)
        try:
            self.tracker.sync(self.tracker_queryset())
        except AttributeError:
            self.tracker.sync()

    def thread_actions(self):
        pass

    def make_thread_form(self):
        self.thread_form = None
        list_choices = self.thread_actions();
        if (not self.request.user.is_authenticated()
            or not list_choices):
            return
        form_fields = {'thread_action': forms.ChoiceField(choices=list_choices)}
        self.thread_form = type('ThreadViewForm', (Form,), form_fields)

    def handle_thread_form(self):
        if self.request.method == 'POST' and self.request.POST.get('origin') == 'thread_form':
            self.thread_form = self.thread_form(self.request.POST, request=self.request)
            if self.thread_form.is_valid():
                action_call = 'thread_action_' + self.thread_form.cleaned_data['thread_action']
                action_extra_args = []
                if ':' in action_call:
                    action_extra_args = action_call[action_call.index(':') + 1:].split(',')
                    action_call = action_call[:action_call.index(':')]
                form_action = getattr(self, action_call)
                try:
                    response = form_action(*action_extra_args)
                    if response:
                        return response
                    return redirect(self.request.path)
                except forms.ValidationError as e:
                    self.message = Message(e.messages[0], messages.ERROR)
            else:
                if 'thread_action' in self.thread_form.errors:
                    self.message = Message(_("Requested action is incorrect."), messages.ERROR)
                else:
                    self.message = Message(form.non_field_errors()[0], messages.ERROR)
        else:
            self.thread_form = self.thread_form(request=self.request)

    def posts_actions(self):
        pass

    def make_posts_form(self):
        self.posts_form = None
        list_choices = self.posts_actions();
        if (not self.request.user.is_authenticated()
            or not list_choices):
            return

        form_fields = {}
        form_fields['list_action'] = forms.ChoiceField(choices=list_choices)
        list_choices = []
        for item in self.posts:
            list_choices.append((item.pk, None))
        if not list_choices:
            return
        form_fields['list_items'] = forms.MultipleChoiceField(choices=list_choices, widget=forms.CheckboxSelectMultiple)
        self.posts_form = type('PostsViewForm', (Form,), form_fields)

    def handle_posts_form(self):
        if self.request.method == 'POST' and self.request.POST.get('origin') == 'posts_form':
            self.posts_form = self.posts_form(self.request.POST, request=self.request)
            if self.posts_form.is_valid():
                checked_items = []
                for post in self.posts:
                    if str(post.pk) in self.posts_form.cleaned_data['list_items']:
                        checked_items.append(post.pk)
                if checked_items:
                    form_action = getattr(self, 'post_action_' + self.posts_form.cleaned_data['list_action'])
                    try:
                        response = form_action(checked_items)
                        if response:
                            return response
                        return redirect(self.request.path)
                    except forms.ValidationError as e:
                        self.message = Message(e.messages[0], messages.ERROR)
                else:
                    self.message = Message(_("You have to select at least one post."), messages.ERROR)
            else:
                if 'list_action' in self.posts_form.errors:
                    self.message = Message(_("Requested action is incorrect."), messages.ERROR)
                else:
                    self.message = Message(self.posts_form.non_field_errors()[0], messages.ERROR)
        else:
            self.posts_form = self.posts_form(request=self.request)

    def __call__(self, request, **kwargs):
        self.request = request
        self.kwargs = kwargs
        self.parents = []
        self.ignored = False
        self.watcher = False
        self.message = request.messages.get_message('threads')
        try:
            self._type_available()
            self.fetch_thread()
            self.check_forum_type()
            self._check_permissions()
            response = self.fetch_posts()
            if response:
                return response
            self.make_thread_form()
            if self.thread_form:
                response = self.handle_thread_form()
                if response:
                    return response
            self.make_posts_form()
            if self.posts_form:
                response = self.handle_posts_form()
                if response:
                    return response
        except (Forum.DoesNotExist, Thread.DoesNotExist):
            return error404(request)
        except ACLError403 as e:
            return error403(request, unicode(e))
        except ACLError404 as e:
            return error404(request, unicode(e))

        # Merge proxy into forum
        self.forum.closed = self.proxy.closed

        return render_to_response('%ss/thread.html' % self.type_prefix,
                                  self._template_vars({
                                        'message': self.message,
                                        'forum': self.forum,
                                        'parents': self.parents,
                                        'thread': self.thread,
                                        'is_read': self.tracker.is_read(self.thread),
                                        'count': self.count,
                                        'posts': self.posts,
                                        'ignored_posts': self.ignored,
                                        'watcher': self.watcher,
                                        'pagination': self.pagination,
                                        'emojis': emojis(),
                                        'quick_reply': QuickReplyForm(request=request),
                                        'thread_form': self.thread_form or None,
                                        'posts_form': self.posts_form or None,
                                      }),
                                  context_instance=RequestContext(request));
