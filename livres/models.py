
from django.db import models
from datetime import date
from datetime import date, timedelta


class Livre(models.Model):

    titre = models.CharField(max_length=200)

    auteur = models.CharField(max_length=150)

    isbn = models.CharField(max_length=20, unique=True)

    categorie = models.CharField(max_length=100)

    annee_publication = models.IntegerField()

    quantite = models.IntegerField(default=1)
    disponible = models.BooleanField(default=True)

    def __str__(self):
        return self.titre
class Emprunt(models.Model):
    livre = models.ForeignKey(Livre, on_delete=models.CASCADE)
    nom_emprunteur = models.CharField(max_length=100) 
    date_emprunt = models.DateField(auto_now_add=True) 
    date_retour_prevue = models.DateField() 
    date_retour_effective = models.DateField(null=True, blank=True)
    rendu = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        
        if not self.id and not self.date_retour_prevue:
            self.date_retour_prevue = date.today() + timedelta(days=14)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.livre.titre} emprunté par {self.nom_emprunteur}"