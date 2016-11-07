from json import dumps as json_dumps
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.shortcuts import redirect
from django.template import RequestContext
from misago import messages

def redirect_message(request, level, message, owner=None):
    messages.add_message(request, level, message, owner)
    return redirect(reverse('index'))


def json_response(request, json=None, status=200, message=None):
    json = json or {}
    json.update({'code': status, 'message': unicode(message)})
    response = json_dumps(json, sort_keys=True,  ensure_ascii=False)
    return HttpResponse(response, content_type='application/json', status=status)
