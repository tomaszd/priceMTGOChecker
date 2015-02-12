from django.views.generic import ListView
from django.core.urlresolvers import reverse
from django.views.generic import CreateView
from contacts.models import Contact
from django.views.generic import UpdateView
from django.views.generic import DeleteView
from django.views.generic import DetailView
import forms
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
# not sure here
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404


class LoggedInMixin(object):

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(LoggedInMixin, self).dispatch(*args, **kwargs)

class ListContactView(LoggedInMixin, ListView):
    model = Contact
    template_name = 'contact_list.html'

    def get_queryset(self):

        return Contact.objects.filter(owner=self.request.user)

class CreateContactView(CreateView):

    model = Contact
    template_name = 'edit_contact.html'
    form_class = forms.ContactForm

class UpdateContactView(UpdateView):

    model = Contact
    template_name = 'edit_contact.html'
    form_class = forms.ContactForm

'''
class CreateContactView(CreateView):
    model = Contact
    template_name = 'edit_contact.html'

    def get_success_url(self):
        return reverse('contacts-list')

    def get_context_data(self, **kwargs):
        context = super(CreateContactView, self).get_context_data(**kwargs)
        print "context", context
        context['action'] = reverse('contacts-new')
        return context

class UpdateContactView(UpdateView):
    model = Contact
    template_name = 'edit_contact.html'
    def get_success_url(self):
        return reverse('contacts-list')

    def get_context_data(self, **kwargs):
        context = super(UpdateContactView, self).get_context_data(**kwargs)
        context['action'] = reverse('contacts-edit',
                                    kwargs={'pk': self.get_object().id})

        return context
'''
class DeleteContactView(DeleteView):
    model = Contact
    template_name = 'delete_contact.html'

    def get_success_url(self):
        return reverse('contacts-list')

class ContactView(LoggedInMixin, DetailView):

    model = Contact
    template_name = 'contact.html'


    def get_object(self, queryset=None):
        """Returns the object the view is displaying.

        """

        if queryset is None:
            queryset = self.get_queryset()

        pk = self.kwargs.get(self.pk_url_kwarg, None)
        queryset = queryset.filter(
            pk=pk,
            owner=self.request.user,
        )

        try:
            obj = queryset.get()
        except ObjectDoesNotExist:
            raise Http404((u"No %(verbose_name)s found matching the query") %
                          {'verbose_name': queryset.model._meta.verbose_name})

        return obj

class EditContactAddressView(UpdateView):

    model = Contact
    template_name = 'edit_addresses.html'
    form_class = forms.ContactAddressFormSet

    def get_success_url(self):

        # redirect to the Contact view.
        return self.get_object().get_absolute_url()
