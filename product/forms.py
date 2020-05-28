from django import forms
from pagedown.widgets import PagedownWidget

from .models import Post, Comment,Profile
from tinymce.widgets import TinyMCE


class TinyMCEWidget(TinyMCE):
    def use_required_attribute(self, *args):
        return False


# class PostForm(forms.ModelForm):
#     overview = forms.CharField(widget=PagedownWidget)
class PostForm(forms.ModelForm):
    content = forms.CharField(
        widget=TinyMCEWidget(
            attrs={'required': False, 'cols': 30, 'rows': 10}
        )
    )
        
        
    class Meta:
        model = Post
        fields = ('title', 'overview','content','thumbnail', 
        'categories', )


class CommentForm(forms.ModelForm):
    content = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'form-control',
        'placeholder': 'Say something...',
        'id': 'usercomment',
        'rows': '4'
    }))
    class Meta:
        model = Comment
        fields = ('content', )

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('first_name', 'last_name', 'email','gender','profile_picture','birth_date','profession','city')