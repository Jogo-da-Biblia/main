from django import forms

from .models import Alternativa, Referencia


class AlternativaForm(forms.ModelForm):
    class Meta:
        model = Alternativa
        fields = '__all__'


class ReferenciaForm(forms.ModelForm):
    class Meta:
        model = Referencia
        fields = '__all__'
