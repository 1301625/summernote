
from django import forms

from .models import Post
from .widgets import DatePickerWidget

from django_summernote.widgets import SummernoteWidget,SummernoteInplaceWidget



class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ['title', 'content','user_max_count','deadline']

        widgets = {
            'content' : SummernoteWidget(attrs={'summernote': {'width': '700px', 'height':'700px'}}),
            'deadline' : DatePickerWidget,
        }


