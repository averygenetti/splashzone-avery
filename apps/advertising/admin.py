from django import forms
from django.contrib import admin
from advertising.models import Ad

# Based this off of the News admin panel.

class AdForm(forms.ModelForm):
    model = Ad
    fields = '__all__'

class AdAdmin(admin.ModelAdmin):
    form = AdForm
    list_display = ['company_name', 'house_ad', 'copy', 'logo', 'url']
    list_editable = ['copy', 'logo', 'url', 'house_ad']


admin.site.register(Ad, AdAdmin)