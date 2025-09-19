#!/usr/bin/env python
"""
Script de test pour vérifier l'API des publications
"""
import os
import sys
import django

# Configuration Django
sys.path.append('backand')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'una.settings')
django.setup()

from api.models import Chercheur, Recherche, RechercheChercheur, RecherchePublication
from api.serializers.chercheur_serializers import ChercheurSerializer
from datetime import date

def test_publication_api():
    """Test pour vérifier que l'API des publications fonctionne"""
    
    print("=== Test de l'API Publications ===")
    
    # Récupérer un chercheur de test
    chercheur = Chercheur.objects.filter(statut='actif').first()
    
    if not chercheur:
        print("❌ Aucun chercheur actif trouvé")
        return
    
    print(f"✅ Chercheur trouvé: {chercheur.prenom} {chercheur.nom}")
    
    # Vérifier s'il a des recherches
    recherches = RechercheChercheur.objects.filter(id_chercheur=chercheur)
    print(f"📚 Recherches associées: {recherches.count()}")
    
    # Compter les publications
    total_publications = 0
    for recherche_chercheur in recherches:
        publications = RecherchePublication.objects.filter(
            id_recherche=recherche_chercheur.id_recherche
        )
        total_publications += publications.count()
        print(f"   - {recherche_chercheur.id_recherche.titre}: {publications.count()} publications")
    
    print(f"📖 Total publications: {total_publications}")
    
    # Tester la sérialisation
    try:
        serializer = ChercheurSerializer(chercheur)
        data = serializer.data
        
        print(f"✅ Sérialisation réussie")
        print(f"📊 Publications dans l'API: {len(data.get('publications', []))}")
        
        # Afficher les titres des publications
        for i, pub in enumerate(data.get('publications', [])[:3], 1):
            print(f"   {i}. {pub['titre'][:60]}...")
            
    except Exception as e:
        print(f"❌ Erreur de sérialisation: {e}")

if __name__ == "__main__":
    test_publication_api()