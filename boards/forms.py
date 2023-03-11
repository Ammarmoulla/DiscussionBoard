from django import forms
from .models import *

class NewTopicForm(forms.ModelForm):
    message = forms.CharField(max_length=4000, widget=forms.Textarea, help_text="that was then")
    class Meta:
        model = Topic
        fields = ["subject", "message"]


class NewPostform(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["message"]