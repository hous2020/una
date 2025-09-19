from rest_framework import serializers
from api.models import Chercheur, ChercheurPoste, Poste, ChercheurReseau, ChercheurDomaineExpertise, Domaine, ChercheurDiplome, RechercheChercheur, RecherchePublication


class DomaineSerializer(serializers.ModelSerializer):
    """Sérialiseur pour le modèle Domaine"""
    
    class Meta:
        model = Domaine
        fields = ['id', 'titre', 'description']


class PosteSerializer(serializers.ModelSerializer):
    """Sérialiseur pour le modèle Poste"""
    
    class Meta:
        model = Poste
        fields = ['id', 'nom', 'abreviation_poste', 'grade']


class ChercheurReseauSerializer(serializers.ModelSerializer):
    """Sérialiseur pour le modèle ChercheurReseau"""
    
    class Meta:
        model = ChercheurReseau
        fields = ['id', 'type_reseau', 'contact']


class ChercheurDomaineExpertiseSerializer(serializers.ModelSerializer):
    """Sérialiseur pour les domaines d'expertise d'un chercheur"""
    
    domaine = DomaineSerializer(source='id_domaine', read_only=True)
    
    class Meta:
        model = ChercheurDomaineExpertise
        fields = ['id', 'domaine']


class RecherchePublicationSerializer(serializers.ModelSerializer):
    """Sérialiseur pour les publications de recherche"""
    
    recherche_titre = serializers.CharField(source='id_recherche.titre', read_only=True)
    
    class Meta:
        model = RecherchePublication
        fields = [
            'id', 'titre', 'resume', 'doi', 'facteur_impact', 
            'date_publication', 'url_publication', 'recherche_titre'
        ]


class ChercheurDiplomeSerializer(serializers.ModelSerializer):
    """Sérialiseur pour les diplômes d'un chercheur"""
    
    class Meta:
        model = ChercheurDiplome
        fields = ['id', 'etablissement', 'diplome', 'annee_obtention']


class ChercheurPosteSerializer(serializers.ModelSerializer):
    """Sérialiseur pour les postes d'un chercheur"""
    
    poste = PosteSerializer(source='id_poste', read_only=True)
    
    class Meta:
        model = ChercheurPoste
        fields = ['id', 'poste']


class ChercheurSerializer(serializers.ModelSerializer):
    """Sérialiseur pour le modèle Chercheur avec ses relations"""
    
    reseaux = serializers.SerializerMethodField()
    postes = serializers.SerializerMethodField()
    domaines_expertise = serializers.SerializerMethodField()
    diplomes = serializers.SerializerMethodField()
    publications = serializers.SerializerMethodField()
    recherches_actuelles = serializers.SerializerMethodField()
    photo_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Chercheur
        fields = [
            'id', 'nom', 'prenom', 'biographie', 'photo_url',
            'statut', 'date_embauche', 'bureau', 'reseaux',
            'postes', 'domaines_expertise', 'diplomes', 'publications', 'recherches_actuelles'
        ]
    
    def get_photo_url(self, obj):
        """Récupère l'URL complète de la photo"""
        if obj.photo and hasattr(obj.photo, 'url'):
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.photo.url)
            return obj.photo.url
        return None
    
    def get_reseaux(self, obj):
        """Récupère les réseaux sociaux du chercheur"""
        reseaux = ChercheurReseau.objects.filter(id_chercheur=obj)
        return ChercheurReseauSerializer(reseaux, many=True).data
    
    def get_postes(self, obj):
        """Récupère les postes du chercheur"""
        postes = ChercheurPoste.objects.filter(id_chercheur=obj)
        return ChercheurPosteSerializer(postes, many=True).data
    
    def get_domaines_expertise(self, obj):
        """Récupère les domaines d'expertise du chercheur"""
        domaines = ChercheurDomaineExpertise.objects.filter(id_chercheur=obj)
        return ChercheurDomaineExpertiseSerializer(domaines, many=True).data
    
    def get_diplomes(self, obj):
        """Récupère les diplômes du chercheur"""
        diplomes = ChercheurDiplome.objects.filter(id_chercheur=obj)
        return ChercheurDiplomeSerializer(diplomes, many=True).data
    
    def get_publications(self, obj):
        """Récupère les publications du chercheur"""
        # Récupérer les recherches liées au chercheur
        recherches_chercheur = RechercheChercheur.objects.filter(id_chercheur=obj)
        publications = []
        
        for recherche_chercheur in recherches_chercheur:
            publications_recherche = RecherchePublication.objects.filter(
                id_recherche=recherche_chercheur.id_recherche
            )
            publications.extend(publications_recherche)
        
        return RecherchePublicationSerializer(publications, many=True).data
    
    def get_recherches_actuelles(self, obj):
        """Récupère les recherches actuelles du chercheur"""
        recherches_chercheur = RechercheChercheur.objects.filter(id_chercheur=obj)
        recherches_actuelles = []
        
        for recherche_chercheur in recherches_chercheur:
            recherche = recherche_chercheur.id_recherche
            # Filtre pour les recherches en cours ou planifiées
            if recherche.statu in ['En cours', 'Planifier']:
                recherches_actuelles.append({
                    'id': recherche.id,
                    'titre': recherche.titre,
                    'description': recherche.description,
                    'statut': recherche.statu,
                    'role_equipe': recherche_chercheur.role_equipe,
                    'date_debut': recherche.date_debut,
                    'date_fin_prevue': recherche.date_fin_prevue,
                })
        
        return recherches_actuelles


class ChercheurListSerializer(serializers.ModelSerializer):
    """Sérialiseur simplifié pour la liste des chercheurs"""
    
    poste_principal = serializers.SerializerMethodField()
    photo_url = serializers.SerializerMethodField()
    specialite = serializers.SerializerMethodField()
    email = serializers.SerializerMethodField()
    reseaux = serializers.SerializerMethodField()
    
    class Meta:
        model = Chercheur
        fields = ['id', 'nom', 'prenom', 'photo_url', 'poste_principal', 'biographie', 'specialite', 'email', 'reseaux']
    
    def get_photo_url(self, obj):
        """Récupère l'URL complète de la photo"""
        if obj.photo and hasattr(obj.photo, 'url'):
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.photo.url)
            return obj.photo.url
        return None
    
    def get_poste_principal(self, obj):
        """Récupère le poste principal du chercheur"""
        poste = ChercheurPoste.objects.filter(id_chercheur=obj).first()
        if poste:
            return poste.id_poste.nom
        return None
    
    def get_specialite(self, obj):
        """Récupère la spécialité principale (premier domaine d'expertise)"""
        domaine = ChercheurDomaineExpertise.objects.filter(id_chercheur=obj).first()
        if domaine:
            return domaine.id_domaine.titre
        return None
    
    def get_email(self, obj):
        """Récupère l'email du chercheur depuis les réseaux"""
        reseau = ChercheurReseau.objects.filter(id_chercheur=obj, type_reseau="Email").first()
        if reseau:
            return reseau.contact
        return None
    
    def get_reseaux(self, obj):
        """Récupère les réseaux sociaux du chercheur"""
        reseaux = ChercheurReseau.objects.filter(id_chercheur=obj)
        return ChercheurReseauSerializer(reseaux, many=True).data