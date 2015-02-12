from django.db import models
from django.core.urlresolvers import reverse

class Contact(models.Model):

    first_name = models.CharField(max_length=255,)
    last_name = models.CharField(max_length=255,)

    email = models.EmailField()


    def get_absolute_url(self):

        return reverse('contacts-view', kwargs={'pk': self.id})

    def __str__(self):

        return ' '.join([
            self.first_name,
            self.last_name,
        ])
