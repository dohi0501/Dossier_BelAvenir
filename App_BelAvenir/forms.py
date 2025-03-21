from django import forms
from django.forms import modelformset_factory
from django.core.exceptions import ValidationError
from .models import *

def pdf_valide (file):
    allowed_mime_types = ['application/pdf']
    if file.content_type not in allowed_mime_types:
        raise ValidationError('Le document doit être un document PDF.')

def img_valide (file):
    allowed_mime_types = ['image/png', 'image/jpeg', 'image/jpg']
    if file.content_type not in allowed_mime_types:
        raise ValidationError('L\'image doit être une image JPEG ou PNG.')

def video_valide (file):
    allowed_mime_types = ['video/mp4']
    if file.content_type not in allowed_mime_types:
        raise ValidationError('La vidéo doit être une vidéo MP4.')
    
def size(file):
    max_size = 10 * 1024 * 1024  # 10 Mo
    if file.size > max_size:
        raise ValidationError(f"Le fichier est trop volumineux. La taille maximale autorisée est de {max_size / (1024 * 1024)} Mo.")


class FormRapprt(forms.ModelForm):
    date_debut = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        required=True
    )
    date_fin = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        required=True
    )
    lieu = forms.CharField(
        widget=forms.TextInput(attrs={'type': 'text', 'placeholder': 'Lieu de la formation'}),
        required=False
    )
    titre = forms.CharField(
        widget=forms.TextInput(attrs={'type': 'text', 'placeholder': 'Titre de la formation'}),
        required=True
    )
    description = forms.CharField(
        widget=forms.Textarea(attrs={'placeholder': 'Description sur la formation', 'rows': 4, 'cols': 50}),
        required=False
    )
    class Meta:
        model = RapportFormation
        fields = ['date_debut', 'date_fin', 'lieu', 'titre', 'description', 'pdf_recapitulatif', 'img_formation']

    pdf_recapitulatif = forms.FileField(validators=[pdf_valide, size])
    img_formation = forms.FileField(validators=[img_valide, size])

class FormImage(forms.ModelForm):
    description = forms.CharField(
        widget=forms.Textarea(attrs={'placeholder': 'Description sur la formation', 'rows': 4, 'cols': 50})
    )
    class Meta:
        model = ImageRapport
        fields = ['rapport' ,'image', 'description']

    image = forms.FileField(validators=[img_valide, size])


class FormVideo(forms.ModelForm):
    description = forms.CharField(
        widget=forms.Textarea(attrs={'placeholder': 'Description sur la formation', 'rows': 4, 'cols': 50})
    )
    class Meta:
        model = VideosRapport
        fields = ['rapport' ,'video', 'description']

    video = forms.FileField(validators=[video_valide, size])