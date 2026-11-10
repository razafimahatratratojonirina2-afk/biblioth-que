
from django import forms
from .models import Livre


class LivreForm(forms.ModelForm):

    class Meta:
        model = Livre

        fields = [
            'titre',
            'auteur',
            'isbn',
            'categorie',
            'annee_publication',
            'quantite'
        ]

        widgets = {
            'titre': forms.TextInput(attrs={
                'class': 'form-control'
            }),

            'auteur': forms.TextInput(attrs={
                'class': 'form-control'
            }),

            'isbn': forms.TextInput(attrs={
                'class': 'form-control'
            }),

            'categorie': forms.TextInput(attrs={
                'class': 'form-control'
            }),

            'annee_publication': forms.NumberInput(attrs={
                'class': 'form-control'
            }),

            'quantite': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0
            }),
        }
