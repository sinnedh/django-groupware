# -*- coding: utf-8 -*-
from django.contrib import messages
from django.contrib.auth import logout
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.utils.translation import ugettext_lazy as _


def logout_view(request):
    logout(request)
    messages.add_message(request, messages.SUCCESS, _('You have been logged out succesfully!'))
    return HttpResponseRedirect(redirect_to=reverse('login'))
