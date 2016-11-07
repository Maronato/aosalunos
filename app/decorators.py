from django.http import HttpResponseRedirect


def is_moderator(function):
    def wrap(request, *args, **kwargs):
        try:
            profile = request.user.profile
            if profile.is_mod:
                return function(request, *args, **kwargs)
        except:
            pass
        return HttpResponseRedirect('/')

    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap
