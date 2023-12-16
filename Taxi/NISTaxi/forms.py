from django import forms

class pumpAttendantForm(forms.Form):
    cardnumber = forms.CharField(label="cardnumber", max_length=16, min_length=16)
    balance = forms.FloatField(label="balance")