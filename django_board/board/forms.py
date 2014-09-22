from django import forms

from .models import Thread, Reply


class ThreadForm(forms.ModelForm):

    class Meta:
        model = Thread
        fields = ['name', 'subj', 'text', 'pic']


class ReplyForm(forms.ModelForm):

    class Meta:
        model = Reply
        fields = ['name', 'subj', 'text', 'pic']
