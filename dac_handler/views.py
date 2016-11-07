
# -*- coding: UTF-8 -*-
from django.shortcuts import redirect, render
from forms import DACInfo
from helpers.register import register
from app.models import Profile
from party.models import Text


def submit(request):
    if request.method == "GET":
        return redirect('/')

    # validate form
    form = DACInfo(request.POST)

    if form.is_valid():

        new_user = register(request, form)

        ra = form.cleaned_data["ra"]
        new_profile = Profile(user=new_user, ra=ra)
        new_profile.save()

    context = {
        'texts': Text().get_text().join(),
        'form': form,
    }
    return render(request, 'app/participe.html', context)
