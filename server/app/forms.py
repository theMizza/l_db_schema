from django import forms


class MakeSQLQueryForm(forms.Form):
    query = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Ваш SQL-запрос',
            'rows': 25
        }),
        label='SQL Запрос'
    )