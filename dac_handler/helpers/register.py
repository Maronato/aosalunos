
# -*- coding: UTF-8 -*-
from django.utils.translation import ugettext as _
from misago import messages
from misago.models import User


def register(request, form):
    need_activation = User.ACTIVATION_USER

    new_user = User.objects.create_user(
        form.cleaned_data['username'],
        form.cleaned_data['email'],
        form.cleaned_data['password1'],
        ip=request.session.get_ip(request),
        agent=request.META.get('HTTP_USER_AGENT'),
        activation=need_activation,
        request=request
    )

    if need_activation == User.ACTIVATION_USER:
        # Mail user activation e-mail
        messages.success(request, _(
            u"%(username)s, sua conta foi criada, mas você precisará confirmar seu email para poder usar o site. Te enviamos um email com seu token de ativação.") % {'username': new_user.username})
        new_user.email_user(
            request,
            'users/activation/user',
            _(u"Olá, %(username)s!") % {
                'username': new_user.username},
        )

    User.objects.resync_monitor()
    return new_user
