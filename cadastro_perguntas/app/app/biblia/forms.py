from django import forms


from .models import Versiculo


class ReferenciaForm(forms.ModelForm):
    class Meta:
        model = Versiculo
        fields = '__all__'


class VersiculoForm(forms.ModelForm):
    class Meta:
        model = Versiculo
        fields = '__all__'
