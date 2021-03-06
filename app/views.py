
# -*- coding: UTF-8 -*-
from django.shortcuts import redirect, render
from party.models import *
from dac_handler.forms import DACInfo
from .models import InfoCookie
from unidecode import unidecode


def index(request):
    context = {
        'texts': Text().get_text().home(),
    }
    response = render(request, 'app/index.html', context)

    cookie = InfoCookie.objects.latest('id')
    try:
        if (cookie.id == int(request.COOKIES.get('info_cookie_id'))):
            return response
    except:
        pass
    value = unidecode(cookie.c_value)
    response.set_cookie("info_cookie", value)
    response.set_cookie("info_cookie_id", cookie.id)
    return response


def about(request):
    context = {
        'texts': Text().get_text().about(),
        'members': Members.objects.all().exclude(name__isnull=True).exclude(name__exact='')
    }
    return render(request, 'app/about.html', context)


def promises(request):
    try:
        promises = Promise.objects.extra(
            select={'titlei': 'CAST(title AS INTEGER)'}
        ).order_by('titlei')
    except:
        promises = Promise.objects.all().order_by(title)

    context = {
        'texts': Text().get_text().promise(),
        'promises': promises,
    }
    return render(request, 'app/propostas.html', context)


def consu(request):
    context = {
        'texts': Text().get_text().consu(),
    }
    return render(request, 'app/consu.html', context)


def join(request):
    context = {
        'texts': Text().get_text().join(),
        'form': DACInfo(),
    }
    return render(request, 'app/participe.html', context)


def logout(request):
    request.session.sign_out(request)
    return redirect('/')
