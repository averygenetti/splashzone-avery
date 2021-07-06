from django import forms
from django.contrib import admin
from wavepool.models import NewsPost


class NewsPostForm(forms.ModelForm):
    model = NewsPost
    fields = '__all__'


class NewsPostAdmin(admin.ModelAdmin):
    form = NewsPostForm


admin.site.register(NewsPost, NewsPostAdmin)
