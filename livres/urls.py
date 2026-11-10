
from django.contrib.auth import views as auth_views
from django.urls import path
from . import views

urlpatterns = [
    # Afficher les livres
    path('', views.liste_livres, name='liste_livres'),

    # Ajouter un livre
    path('ajouter/', views.ajouter_livre, name='ajouter_livre'),

    # Modifier un livre
    path('modifier/<int:id>/', views.modifier_livre, name='modifier_livre'),
    # supprimer un livre
    path('supprimer/<int:id>/', views.supprimer_livre, name='supprimer_livre'),
    # emprunter un livre
   path('emprunts/', views.liste_emprunts, name='liste_emprunts'),
   path('emprunter/<int:id>/', views.emprunter_livre, name='emprunter_livre'),
   path('retourner/<int:id>/', views.retourner_livre, name='retourner_livre'),
   path('connexion/', auth_views.LoginView.as_view(template_name='livres/login.html'), name='connexion'),
   path('deconnexion/', auth_views.LogoutView.as_view(), name='deconnexion'),
]
