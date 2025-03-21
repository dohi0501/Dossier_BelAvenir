from django.db import models
from django.contrib.auth.models import User
import os
from django.conf import settings

# Create your models here.

class RapportFormation(models.Model):
    date_debut = models.DateField(null=True, blank=True)
    date_fin = models.DateField(null=True, blank=True)
    lieu = models.CharField(max_length=220, default='abidjan')
    titre = models.CharField(null=False, blank=False, max_length=225)
    description = models.TextField(blank=False, null=False)
    pdf_recapitulatif = models.FileField(upload_to='doc_pdf/', blank=True, null=True)
    img_formation = models.ImageField(upload_to='doc_img_formation/', default='doc_img_formation/img.png', blank=True, null=True)
    save_date = models.DateTimeField(auto_now_add=True)
    save_by = models.ForeignKey(User, on_delete=models.PROTECT)

    def __str__(self):
        return f'{self.id} - {self.titre}'
    
    def delete(self, *args, **kwargs):
        if self.pdf_recapitulatif:
            pdf_path = os.path.join(settings.MEDIA_ROOT, str(self.pdf_recapitulatif))
            if os.path.exists(pdf_path):
                os.remove(pdf_path)

        super().delete(*args, **kwargs)
    
    class Meta:
        ordering = ['-save_date']



class ImageRapport(models.Model):
    rapport = models.ForeignKey(RapportFormation, on_delete=models.CASCADE)
    image = models.FileField(upload_to='doc_img/', blank=False, null=False)
    description = models.ImageField(blank=False, null=False)
    save_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'rapport N°{self.rapport.id} - image {self.id}'
    
    class Meta:
        ordering = ['-save_date']



class VideosRapport(models.Model):
    rapport = models.ForeignKey(RapportFormation, on_delete=models.CASCADE)
    video = models.FileField(upload_to='doc_video/', blank=False, null=False)
    description = models.TextField(blank=False, null=False)
    save_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'rapport N°{self.rapport.id} - vidéo {self.id}'
    
    class Meta:
        ordering = ['-save_date']
