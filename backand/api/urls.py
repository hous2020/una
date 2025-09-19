from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ChercheurViewSet,
    LaboratoireParcourViewSet,
    CandidatureParcoursViewSet,
    LaboratoireViewSet,
    RecherchePublicationViewSet,
)

# Création du routeur pour l'API
routeur = DefaultRouter()
routeur.register(r'chercheurs', ChercheurViewSet)
routeur.register(r'laboratoires', LaboratoireViewSet)
routeur.register(r'parcours', LaboratoireParcourViewSet)
routeur.register(r'candidatures', CandidatureParcoursViewSet)
routeur.register(r'publications', RecherchePublicationViewSet)

urlpatterns = [
    path('', include(routeur.urls)),
]