from datetime import date
from django.contrib.auth.decorators import login_required
from django.db import models  # Indispensable pour les filtres complexes (Q)
from django.shortcuts import get_object_or_404, redirect, render
from .forms import LivreForm
from .models import Emprunt, Livre


def liste_livres(request):
    # Récupérer le terme de recherche depuis l'URL (si l'utilisateur a cherché quelque chose)
    query = request.GET.get('q')

    if query:
        # Filtrer les livres dont le titre, l'auteur ou la catégorie contient le mot-clé (insensible à la casse)
        livres = Livre.objects.filter(
            models.Q(titre__icontains=query)
            | models.Q(auteur__icontains=query)
            | models.Q(categorie__icontains=query)
        )
    else:
        livres = Livre.objects.all()

    return render(
        request, 'livres/liste.html', {'livres': livres, 'query': query}
    )


@login_required
def ajouter_livre(request):
    if request.method == 'POST':
        form = LivreForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('liste_livres')
    else:
        form = LivreForm()

    return render(request, 'livres/ajouter.html', {'form': form})


@login_required
def modifier_livre(request, id):
    livre = get_object_or_404(Livre, id=id)

    if request.method == 'POST':
        form = LivreForm(request.POST, instance=livre)

        if form.is_valid():
            form.save()
            return redirect('liste_livres')

    else:
        form = LivreForm(instance=livre)

    return render(request, 'livres/modifier.html', {'form': form, 'livre': livre})


@login_required
def supprimer_livre(request, id):
    livre = get_object_or_404(Livre, id=id)

    if request.method == 'POST':
        livre.delete()
        return redirect('liste_livres')

    return render(request, 'livres/supprimer.html', {'livre': livre})


@login_required
def liste_emprunts(request):
    emprunts = Emprunt.objects.filter(rendu=False)
    return render(request, 'livres/emprunts.html', {'emprunts': emprunts})


@login_required
def emprunter_livre(request, id):
    livre = get_object_or_404(Livre, id=id)

    if request.method == 'POST':
        nom = request.POST.get('nom_emprunteur')
        
        # Vérification anti-doublon : cette personne a-t-elle déjà emprunté ce livre sans l'avoir rendu ?
        deja_emprunte = Emprunt.objects.filter(livre=livre, nom_emprunteur=nom, rendu=False).exists()
        
        if deja_emprunte:
            return render(request, 'livres/form_emprunt.html', {
                'livre': livre, 
                'erreur': "Cette personne a déjà un emprunt en cours pour ce livre !"
            })

        # S'il reste du stock, on autorise l'emprunt
        if livre.quantite > 0:
            livre.quantite -= 1
            livre.save()

            Emprunt.objects.create(livre=livre, nom_emprunteur=nom)
            return redirect('liste_emprunts')
        else:
            return render(request, 'livres/form_emprunt.html', {
                'livre': livre, 
                'erreur': "Ce livre n'est plus en stock."
            })

    return render(request, 'livres/form_emprunt.html', {'livre': livre})


@login_required
def retourner_livre(request, id):
    emprunt = get_object_or_404(Emprunt, id=id)
    if not emprunt.rendu:
        emprunt.rendu = True
        emprunt.date_retour_effective = date.today()
        emprunt.save()

        emprunt.livre.quantite += 1
        emprunt.livre.save()

    return redirect('liste_emprunts')