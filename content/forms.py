
from django import forms

from .models import Post ,Comment
from .widgets import DatePickerWidget


from django_summernote.widgets import SummernoteWidget,SummernoteInplaceWidget



class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ['title', 'content', 'user_max_count', 'deadline']

        widgets = {
            'content' : SummernoteWidget(attrs={'summernote': {'width': '700px', 'height':'700px'}}),
            'deadline' : DatePickerWidget,
        }


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ['context']

        widgets = {
            'context' : forms.TextInput(attrs={'class':'comment-form', 'placeholder': '댓글 달기..' ,'size': '70px'}),
        }

    # context = forms.CharField(label='', widget=forms.TextInput(attrs={
    #      'class' : 'comment-form',
    #      'size' : '70px',
    #      'placeholder': '댓글 달기..',

            #'content': SummernoteWidget(attrs={'summernote': {'width': '300px', 'height': '300px'}}),
    # }))
