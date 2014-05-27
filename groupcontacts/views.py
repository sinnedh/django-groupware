from django.shortcuts import render

from django.views.generic import ListView, DetailView
from django.utils.translation import ugettext_lazy as _

from django.views.generic.edit import CreateView, UpdateView, DeleteView

from groupcontacts.models import Contact
from groupcontacts.forms import ContactAddForm


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


class ContactUpdate(UpdateView):
    form_class = ContactAddForm
    model = Contact

    def get_context_data(self, **kwargs):
        context = super(ContactUpdate, self).get_context_data(**kwargs)
        context['title'] = _('Manage Contacts')
        context['subtitle'] = _('Update')
        return context
