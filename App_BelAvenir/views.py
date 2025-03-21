from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.decorators import user_passes_test, login_required
from .forms import *
from .models import *
import mimetypes 

# Create your views here.

# identification
def is_admin(user):
    return user.is_authenticated and user.is_staff and user.is_superuser

def accueil(request, *args, **kwargs):
    rap = RapportFormation.objects.all()
    return render(request, 'index.html', {
        'rapport': rap,
    })

def generalite_vih(request, *args, **kwargs):
    return render(request, 'generalite_vih.html')

def cycle_vih(request, *args, **kwargs):
    return render(request, 'cycle_vih.html')

def reacton_corps_vih(request, *args, **kwargs):
    return render(request, 'reaction_corps.html')

def apres_infection_vih(request, *args, **kwargs):
    return render(request, 'apres_infection.html')

def generalite_ist(request, *args, **kwargs):
    return render(request, 'generalite_ist.html')

def apropos(request, *args, **kwargs):
    return render(request, 'apropos.html')

def projets(request, *args, **kwargs):
    return render(request, 'projets.html')

# Administration 
def login_admin(request, *args, **kwargs):
    if request.method == 'POST':

        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():

            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(request, username=username, password=password)

            if user is not None:
                try:
                    login(request, user)
                    return redirect('administration', username=username)
                
                except:
                    erreur = 'une erreur est survenue!'
                    return render(request, 'login_administration.html', {'form': form, 'error': erreur})

            
            else:
                erreur = 'une erreur est survenue!'
                return render(request, 'login_administration.html', {'form': form, 'error': erreur})
        
        else:
            erreur = 'nom ou mot de passe invalide!'
            return render(request, 'login_administration.html', {'form': form, 'error': erreur})

    else:
        form = AuthenticationForm()
        return render(request, 'login_administration.html', {'form': form})
    


@login_required(login_url='login_Administration/')
@user_passes_test(is_admin)
def administration (request, username, *args, **kwargs):
    user = User.objects.get(username=username)
    rap = RapportFormation.objects.all()
    vid = VideosRapport.objects.all()
    img = ImageRapport.objects.all()
    return render(request, 'administration.html', {
        'user': user,
        'rap': rap,
        'img': img,
        'vid': vid,
    })



@login_required(login_url='login_Administration/')
@user_passes_test(is_admin)
def Ajout_rapport(request, username, *args, **kwargs):
    user = User.objects.get(username=username)

    if request.method == 'POST':

        Form_R = FormRapprt(request.POST, request.FILES)

        if Form_R.is_valid():

            if Form_R.cleaned_data.get('date_debut') >= Form_R.cleaned_data.get('date_fin'):
                erreur = 'La date de fin doit être supérieure à la date de début.'
                Form_R = FormRapprt(request.POST, request.FILES)
                return render(request, 'ajout_rapport.html', {'form': Form_R, 'error': erreur})
            
            else:
                rapport = Form_R.save(commit=False)
                rapport.save_by = user
                rapport.save()

                return redirect('administration', username=username)
        
        else:

            Form_R = FormRapprt(request.POST, request.FILES)
            erreur = 'formulaire invalide vérifier les données du formulaire'
            return render(request, 'ajout_rapport.html', {'form': Form_R, 'error': erreur})
        
    else:
        Form_R = FormRapprt()
    
    return render(request, 'ajout_rapport.html', {'form': Form_R})
    

@login_required(login_url='login_Administration/')
@user_passes_test(is_admin)
def liste_rapport(request, username, *args, **kwargs):
    user = User.objects.get(username=username)
    listes = RapportFormation.objects.all()

    return render(request, 'liste_rapports.html', {'liste': listes, 'user': user})


@login_required(login_url='login_Administration/')
@user_passes_test(is_admin)
def Modifier_rapport(request, username, id, *args, **kwargs):
    user = User.objects.get(username=username)

    rapport = get_object_or_404(RapportFormation, id=id)

    if request.method == 'POST':
        form = FormRapprt(request.POST, instance=rapport)

        if form.is_valid():
            rap = form.save(commit=False)
            rap.save_by = user
            rap.save()
            messages.success(request, f' le rapport N°{rapport.id} a été modifié avec succès')
            return redirect('liste_rapport', username=username)
        else:
            messages.error(request, 'formulaire invalide!')

    else:
        form = FormRapprt(instance=rapport)
    
    return render(request, 'modifier_rapport.html', {'form': form, 'rap': rapport})


@login_required(login_url='login_Administration/')
@user_passes_test(is_admin)
def Ajout_image(request, username, *args, **kwargs):
    user = User.objects.get(username=username)

    if request.method == 'POST':
        form = FormImage(request.POST, request.FILES)

        if form.is_valid(): 
            img = form.save(commit=False)
            img.save_by = user
            img.save()
            messages.success(request, "image enregistrée avec succès!")
            return redirect('ajout_image', username=username)

        else:

            form = FormImage(request.POST, request.FILES)
            erreur = 'formulaire invalide vérifier les données du formulaire'
            return render(request, 'ajout_image.html', {'form': form, 'error': erreur})

    else:

        form = FormImage()
    
    return render(request, 'ajout_image.html', {'form': form})


@login_required(login_url='login_Administration/')
@user_passes_test(is_admin)
def liste_image(request, username, *args, **kwargs):
    user = User.objects.get(username=username)
    listes = ImageRapport.objects.all()

    return render(request, 'liste_images.html', {'liste': listes, 'user': user})


@login_required(login_url='login_Administration/')
@user_passes_test(is_admin)
def Modifier_image(request, username, id, *args, **kwargs):
    user = User.objects.get(username=username)

    image =get_object_or_404(ImageRapport, id=id)

    if request.method == 'POST':
        form = FormImage(request.POST, instance=image)

        if form.is_valid():
            img = form.save(commit=False)
            img.save_by = user
            img.save()
            messages.success(request, f'l\'image N°{image.id} a été modifier avec succès')
            return redirect('liste_image', username=username)
        
        else:
            messages.error(request, 'formulaire invalide!')

    else:
        form = FormImage(instance=image)

    return render(request, 'modifier_image.html', {'form': form, 'img': image})



@login_required(login_url='login_Administration/')
@user_passes_test(is_admin)
def Ajout_video(request, username, *args, **kwargs):
    user = User.objects.get(username=username)

    if request.method == 'POST':
        form = FormVideo(request.POST, request.FILES)

        if form.is_valid(): 

            img = form.save(commit=False)
            img.save_by = user
            img.save()
            messages.success(request, "vidéo enregistrée avec succès!")
            return redirect('ajout_video', username=username)
        
        else:

            form = FormVideo(request.POST, request.FILES)
            erreur = 'formulaire invalide vérifier les données du formulaire'
            return render(request, 'ajout_video.html', {'form': form, 'error': erreur})

    else:

        form = FormVideo()
        
    return render(request, 'ajout_video.html', {'form': form})


@login_required(login_url='login_Administration/')
@user_passes_test(is_admin)
def liste_video(request, username, *args, **kwargs):
    user = User.objects.get(username=username)
    listes = VideosRapport.objects.all()

    return render(request, 'liste_videos.html', {'liste': listes, 'user': user})



@login_required(login_url='login_Administration/')
@user_passes_test(is_admin)
def Modifier_video(request, id, username, *args, **kwargs):
    user = User.objects.get(username=username)

    video = get_object_or_404(VideosRapport, id=id)

    if request.method == 'POST':

        form = FormVideo(request.POST, instance=video)

        if form.is_valid():
            vid = form.save(commit=False)
            vid.save_by = user
            vid.save()
            messages.success(request, f'la vidéo N°{vid.id} a été modifier avec succès')
            return redirect('liste_video', username=username)
        
        else:
            messages.error(request, 'formulaire invalide')

    else:
        form = FormVideo(instance=video)
        return render(request, 'modifier_video.html', {'form': form, 'vid_id': video})






@login_required(login_url='login_Administration/')
@user_passes_test(is_admin)
def logout_user (request, *args, **kwargs):
    logout(request)
    return redirect('accueil')



def erreur_404(request, exception):
    return render(request, '404.html', status=404)
