from django import forms


from .models import Versiculo, Livro


class ReferenciaForm(forms.ModelForm):
    class Meta:
        model = Versiculo
        fields = '__all__'


