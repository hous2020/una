from rest_framework import serializers
from api.models import (
    RecherchePublication,
    RecherchePublicationMotCle,
    RecherchePublicationCitation,
    RechercheChercheur,
)


class PublicationMotCleSerializer(serializers.ModelSerializer):
    """Sérialiseur pour les mots-clés d'une publication"""

    class Meta:
        model = RecherchePublicationMotCle
        fields = ["id", "mot_cle"]


class PublicationCitationSerializer(serializers.ModelSerializer):
    """Sérialiseur pour les citations d'une publication"""

    class Meta:
        model = RecherchePublicationCitation
        fields = ["id", "citation"]


class RechercheChercheurPublicationSerializer(serializers.ModelSerializer):
    """Sérialiseur pour les chercheurs sur une publication"""
    nom_complet = serializers.SerializerMethodField()
    role = serializers.CharField(source='role_equipe')

    class Meta:
        model = RechercheChercheur
        fields = ['nom_complet', 'role']

    def get_nom_complet(self, obj):
        return f"{obj.id_chercheur.prenom} {obj.id_chercheur.nom}"


class RecherchePublicationListSerializer(serializers.ModelSerializer):
    """Sérialiseur liste des publications"""

    fichier_url = serializers.SerializerMethodField()
    recherche_titre = serializers.CharField(source="id_recherche.titre", read_only=True)
    citations_count = serializers.SerializerMethodField()
    chercheurs = serializers.SerializerMethodField()

    class Meta:
        model = RecherchePublication
        fields = [
            "id",
            "titre",
            "resume",
            "doi",
            "facteur_impact",
            "date_publication",
            "url_publication",
            "fichier_url",
            "recherche_titre",
            "citations_count",
            "chercheurs",
        ]

    def get_fichier_url(self, obj):
        if obj.fichier and hasattr(obj.fichier, "url"):
            request = self.context.get("request")
            if request:
                return request.build_absolute_uri(obj.fichier.url)
            return obj.fichier.url
        return None

    def get_citations_count(self, obj):
        return RecherchePublicationCitation.objects.filter(id_recherche_publication=obj).count()

    def get_chercheurs(self, obj):
        chercheurs_associes = RechercheChercheur.objects.filter(id_recherche=obj.id_recherche)
        return RechercheChercheurPublicationSerializer(chercheurs_associes, many=True).data


class RecherchePublicationDetailSerializer(serializers.ModelSerializer):
    """Sérialiseur détail d'une publication avec relations"""

    fichier_url = serializers.SerializerMethodField()
    mots_cles = serializers.SerializerMethodField()
    citations = serializers.SerializerMethodField()
    recherche_titre = serializers.CharField(source="id_recherche.titre", read_only=True)

    class Meta:
        model = RecherchePublication
        fields = [
            "id",
            "titre",
            "resume",
            "contenu",
            "doi",
            "facteur_impact",
            "date_publication",
            "url_publication",
            "fichier_url",
            "recherche_titre",
            "mots_cles",
            "citations",
        ]

    def get_fichier_url(self, obj):
        if obj.fichier and hasattr(obj.fichier, "url"):
            request = self.context.get("request")
            if request:
                return request.build_absolute_uri(obj.fichier.url)
            return obj.fichier.url
        return None

    def get_mots_cles(self, obj):
        qs = RecherchePublicationMotCle.objects.filter(id_recherche_publication=obj)
        return PublicationMotCleSerializer(qs, many=True).data

    def get_citations(self, obj):
        qs = RecherchePublicationCitation.objects.filter(id_recherche_publication=obj)
        return PublicationCitationSerializer(qs, many=True).data
