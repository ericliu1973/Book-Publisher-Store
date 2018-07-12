from django import forms

PRODUCT_QUAN_CHOICE = [(i, str(i)) for i in range (1,30)]

class CartAddForm(forms.Form):
    quantity= forms.TypedChoiceField(choices=PRODUCT_QUAN_CHOICE,coerce=int)
    update = forms.BooleanField(required=False,initial=False,widget=forms.HiddenInput)


