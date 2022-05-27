from .models import Comment, CwUsers
from django import forms


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('content',)


class CritticWarsForm(forms.ModelForm):
    class Meta:
        model = CwUsers
        fields = ('cw_id', 'cw_name',)

        labels = {
            'cw_name': 'CritticWars Name',
            'cw_id': 'CritticWars ID'
        }

        error_messages = {
            'cw_name': {
                'max_length': "Name is too long.",
            },
        }
