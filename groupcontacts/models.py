from django.db import models
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _


class Contact(models.Model):
    title = models.CharField(max_length=200, blank=True, null=True)
    firstname = models.CharField(max_length=200)
    lastname = models.CharField(max_length=200)
    birthdate = models.DateField(_('Birthdate'), blank=True, null=True)
    note = models.TextField(_('Note'), blank=True, null='True')

#    def get_absolute_url(self):
#        return reverse('groupcontacts:contact_detail', kwargs={'pk': self.pk})

    def __unicode__(self):
        return self.fullname()

    def fullname(self):
        name = '%s %s' % (self.firstname, self.lastname)
        if self.title:
            name = '%s %s' % (self.title, name)
        return name


class Address(models.Model):
    contact = models.ForeignKey(Contact)
    street = models.CharField(max_length=200, blank=True, null=True)
    additional = models.CharField(max_length=200, blank=True, null=True)
    postcode = models.CharField(max_length=20, blank=True, null=True)
    city = models.CharField(max_length=200, blank=True, null=True)
    country = models.CharField(max_length=200, blank=True, null=True)

