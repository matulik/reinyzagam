from django.shortcuts import render
from django.shortcuts import redirect, render_to_response, RequestContext

from User.models import Login

def choose(request):
    if Login.auth(request):
        return render_to_response('webapp/choose.html', context_instance=RequestContext(request))
    else:
        msg = u'You are logged out. Please login first.'
        return render_to_response('login.html', { 'msg': msg }, context_instance=RequestContext(request))

def locations(request):
    if Login.auth(request):
        return render_to_response('webapp/locations.html', context_instance=RequestContext(request))

    else:
        msg = u'You are logged out. Please login first.'
        return render_to_response('login.html', context_instance=RequestContext(request))