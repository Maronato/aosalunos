
# -*- coding: UTF-8 -*-
from django.shortcuts import redirect, render
from django.core.urlresolvers import reverse
from .forms import *
from .models import *
from app.decorators import is_moderator
from misago import messages


@is_moderator
def index(request):
    return render(request, 'party/index.html')


@is_moderator
def promises(request):
    form = AddPromise()
    promises = Promise.objects.all()
    return render(request, 'party/promises.html', {'form': form, 'promises': promises})


@is_moderator
def add_promises(request):
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = AddPromise(request.POST)
        # check whether it's valid:
        if form.is_valid():
            new_promise = Promise(
                            title=form.cleaned_data['title'],
                            text=form.cleaned_data['text']
                            )
            new_promise.save()
            messages.success(request, ("Proposta adicionada!"))
            return redirect(reverse('party_promises'))

        else:
            return render(request, 'party/promises.html', {'form': form})

    return redirect(reverse('party_promises'))


@is_moderator
def edit_promises(request):
    if request.method == 'POST':
        p_id = request.POST['id']
        title = request.POST['title']
        text = request.POST['text']
        promise = Promise.objects.get(pk=p_id)
        promise.title, promise.text = title, text
        promise.save()
        messages.success(request, ("Proposta alterada!"))
    return redirect(reverse('party_promises'))


@is_moderator
def delete_promises(request):
    if request.method == 'POST':
        p_id = request.POST['id']
        Promise.objects.get(pk=p_id).delete()
        messages.success(request, ("Proposta apagada!"))
    return redirect(reverse('party_promises'))


@is_moderator
def texts(request):
    if request.method == 'POST':
        text_type = request.POST['id']
        title1 = request.POST['title1']
        text1 = request.POST['text1']
        title2 = request.POST['title2']
        text2 = request.POST['text2']
        texts = Text().get_text()

        if text_type == "home":
            texts.home_1_title, texts.home_1_text, texts.home_2_title, texts.home_2_text = title1, text1, title2, text2
        elif text_type == "consu":
            texts.consu_1_title, texts.consu_1_text, texts.consu_2_title, texts.consu_2_text = title1, text1, title2, text2
        elif text_type == "about":
            texts.us_1_title, texts.us_1_text, texts.us_2_title, texts.us_2_text = title1, text1, title2, text2
        elif text_type == "join":
            texts.join_1_title, texts.join_1_text, texts.join_2_title, texts.join_2_text = title1, text1, title2, text2
        elif text_type == "promise":
            texts.promise_1_title, texts.promise_1_text, texts.promise_2_title, texts.promise_2_text = title1, text1, title2, text2
        else:
            dfdg
        texts.save()
        messages.success(request, ("Textos alterados!"))
        return redirect(reverse('party_texts'))

    texts = {
            'home': Text().get_text().home(),
            'consu': Text().get_text().consu(),
            'about': Text().get_text().about(),
            'join': Text().get_text().join(),
            'promise': Text().get_text().promise(),
    }
    return render(request, 'party/texts.html', {'texts': texts})


@is_moderator
def profile(request):
    instance = request.user.profile.members
    form = EditProfile(request.POST or None, instance=instance)
    if form.is_valid():
        messages.success(request, (u"Informações alteradas!"))
        form.save()
    return render(request, 'party/profile.html', {'form': form})


@is_moderator
def blog(request):
    form = AddPromise()
    return render(request, 'party/blog.html', {'form': form})
