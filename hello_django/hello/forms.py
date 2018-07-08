from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields=('content',)


class SearchForm(forms.Form):
    search_type_choice=(
        (0,'Author'),(1,'Book Title')
    )
    search_type = forms.IntegerField(widget=forms.widgets.Select(choices=search_type_choice,attrs={'class':'form-control'}))
    search_words=forms.CharField(error_messages={'required':'pls input search words'})


class EmailForm(forms.Form):
    person = forms.CharField(max_length=40,widget=forms.TextInput(attrs={'class':'form-control','placeholder':"friend's name",'required':'required',}))
    info = forms.CharField( widget=forms.Textarea(attrs={'class':'form-control','placeholder':'please write something to your firend','required':"required"}))
    to = forms.EmailField(widget=forms.TextInput(attrs={"class":"form-control","placeholder":"friend@mailaddress",'required':'required',}))