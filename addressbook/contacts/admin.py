from django.contrib import admin
from django.contrib.contenttypes import generic


from contacts.models import Contact
from contacts.models import Address


class ContactAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'email', 'owner', 'get_absolute_url', 'address_set')
    # list_filter = ('version', 'hidden', 'important')
    # inlines = (CommentInline,)
   # search_fields = ('umbrella_task__key',)
#  task_summary.admin_order_field = 'umbrella_task__summary'

admin.site.register(Contact, ContactAdmin)


class AddressAdmin(admin.ModelAdmin):
    list_display = ('contact',
                   'address_type',
                   'address',
                   'city',
                   'state',
                   'postal_code')


admin.site.register(Address, AddressAdmin)
