from django.contrib import admin
from .models import *

# Register your models here.

class AfficheRapports(admin.ModelAdmin):
    list_display = ('date_debut', 'date_fin', 'titre', 'description', 'pdf_recapitulatif')

class AfficheImages(admin.ModelAdmin):
    list_display = ('rapport', 'image', 'description')


class AfficheVideos(admin.ModelAdmin):
    list_display = ('rapport', 'video', 'description')


admin.site.register(RapportFormation, AfficheRapports)
admin.site.register(ImageRapport, AfficheImages)
admin.site.register(VideosRapport, AfficheVideos)