from django.shortcuts import render

from django.views.generic import ListView, DetailView
from django.utils.translation import ugettext_lazy as _

from groupcontacts.models import Contact


class ContactList(ListView):
    model = Contact

    def get_context_data(self, **kwargs):
        context = super(ContactList, self).get_context_data(**kwargs)
        context['title'] = _('Manage contacts')
        context['subtitle'] = _('List')
        return context


class ContactDetail(DetailView):
    model = Contact

    def get_context_data(self, **kwargs):
        context = super(ContactDetail, self).get_context_data(**kwargs)
        context['title'] = _('Manage contacts')
        context['subtitle'] = _('Details')
        return context
