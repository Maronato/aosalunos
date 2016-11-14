
# -*- coding: UTF-8 -*-
from django.shortcuts import redirect, render
from party.models import *
from dac_handler.forms import DACInfo


def index(request):
    context = {
        'texts': Text().get_text().home(),
    }
    return render(request, 'app/index.html', context)


def about(request):
    context = {
        'texts': Text().get_text().about(),
        'members': Members.objects.all().exclude(name__isnull=True).exclude(name__exact='')
    }
    return render(request, 'app/about.html', context)


def promises(request):
    context = {
        'texts': Text().get_text().promise(),
        'promises': Promise.objects.all(),
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
