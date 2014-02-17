from django.contrib import admin
from prices.models import Color

# Register your models here.



class ColorAdmin(admin.ModelAdmin):
    fields = [ 'color']

admin.site.register(Color, ColorAdmin)