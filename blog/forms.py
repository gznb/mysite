from django import forms
from .models import Comment

#  表单验证，和 rest 有很大的相似性


class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=25)
    email = forms.EmailField()
    to = forms.EmailField()

    # widget 小部件，使用一个在页面的时候，不再是char而是Textarea
    # required=False 表示这个字段不是一定要 填上的
    comments = forms.CharField(required=False, widget=forms.Textarea)


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'email', 'body')
