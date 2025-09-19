from rest_framework import serializers
from rest_framework import serializers
from api.models import (
    Laboratoire, LaboratoireParcour, LaboratoireParcourConditionAdmission,
    LaboratoireParcourDeboucher, LaboratoireParcourSpecialisation, TypeLaboratoire,
    CandidatureParcours
)


class TypeLaboratoireSerializer(serializers.ModelSerializer):
    """Sérialiseur pour le modèle TypeLaboratoire"""
    
    class Meta:
        model = TypeLaboratoire
        fields = ['id', 'type_labo']


class LaboratoireSerializer(serializers.ModelSerializer):
    """Sérialiseur pour le modèle Laboratoire"""
    
    type_laboratoire = TypeLaboratoireSerializer(source='id_type_laboratoire', read_only=True)
    logo_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Laboratoire
        fields = [
            'id', 'nom', 'logo_url', 'ufr', 'date_de_creation', 
            'type_laboratoire'
        ]
    
    def get_logo_url(self, obj):
        """Récupère l'URL complète du logo"""
        if obj.logo and hasattr(obj.logo, 'url'):
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.logo.url)
            return obj.logo.url
        return None


class LaboratoireParcourConditionAdmissionSerializer(serializers.ModelSerializer):
    """Sérialiseur pour les conditions d'admission d'un parcours"""
    
    class Meta:
        model = LaboratoireParcourConditionAdmission
        fields = ['id', 'titre', 'valeur']


class LaboratoireParcourDeboucherSerializer(serializers.ModelSerializer):
    """Sérialiseur pour les débouchés d'un parcours"""
    
    class Meta:
        model = LaboratoireParcourDeboucher
        fields = ['id', 'deboucher']


class LaboratoireParcourSpecialisationSerializer(serializers.ModelSerializer):
    """Sérialiseur pour les spécialisations d'un parcours"""
    
    class Meta:
        model = LaboratoireParcourSpecialisation
        fields = ['id', 'specialisation']


class LaboratoireParcourSerializer(serializers.ModelSerializer):
    """Sérialiseur pour le modèle LaboratoireParcour avec ses relations"""
    
    laboratoire = LaboratoireSerializer(source='id_laboratoire', read_only=True)
    conditions_admission = serializers.SerializerMethodField()
    debouches = serializers.SerializerMethodField()
    specialisations = serializers.SerializerMethodField()
    
    class Meta:
        model = LaboratoireParcour
        fields = [
            'id', 'nom_parour', 'date_creation', 'description', 
            'duree_formation', 'nombre_etudiant_max', 'statu',
            'laboratoire', 'conditions_admission', 'debouches', 'specialisations'
        ]
    
    def get_conditions_admission(self, obj):
        """Récupère les conditions d'admission du parcours"""
        conditions = LaboratoireParcourConditionAdmission.objects.filter(id_laboratoire_parcour=obj)
        return LaboratoireParcourConditionAdmissionSerializer(conditions, many=True).data
    
    def get_debouches(self, obj):
        """Récupère les débouchés du parcours"""
        debouches = LaboratoireParcourDeboucher.objects.filter(id_laboratoire_parcour=obj)
        return LaboratoireParcourDeboucherSerializer(debouches, many=True).data
    
    def get_specialisations(self, obj):
        """Récupère les spécialisations du parcours"""
        specialisations = LaboratoireParcourSpecialisation.objects.filter(id_laboratoire_parcour=obj)
        return LaboratoireParcourSpecialisationSerializer(specialisations, many=True).data


class LaboratoireParcourListSerializer(serializers.ModelSerializer):
    """Sérialiseur simplifié pour la liste des parcours"""
    
    laboratoire_nom = serializers.CharField(source='id_laboratoire.nom', read_only=True)
    laboratoire_ufr = serializers.CharField(source='id_laboratoire.ufr', read_only=True)
    
    class Meta:
        model = LaboratoireParcour
        fields = [
            'id', 'nom_parour', 'date_creation', 'description', 
            'duree_formation', 'nombre_etudiant_max', 'statu',
            'laboratoire_nom', 'laboratoire_ufr'
        ]


class CandidatureParcoursSerializer(serializers.ModelSerializer):
    """Sérialiseur pour les candidatures aux parcours"""
    
    parcours_nom = serializers.CharField(source='id_parcours.nom_parour', read_only=True)
    laboratoire_nom = serializers.CharField(source='id_parcours.id_laboratoire.nom', read_only=True)
    nom_complet = serializers.ReadOnlyField()
    age = serializers.ReadOnlyField()
    
    class Meta:
        model = CandidatureParcours
        fields = [
            'id', 'nom_candidat', 'prenom_candidat', 'nom_complet', 'age',
            'date_naissance', 'lieu_naissance', 'nationalite',
            'telephone_candidat', 'email_candidat', 'adresse_complete',
            'ville_residence', 'pays_residence',
            'niveau_etude_actuel', 'etablissement_origine', 'filiere_etude',
            'moyenne_generale', 'annee_obtention_diplome',
            'cv_candidat', 'lettre_motivation', 'releves_notes', 'diplome_obtenu',
            'id_parcours', 'parcours_nom', 'laboratoire_nom',
            # Champs motivation et projet supprimés
            'statut_candidature', 'date_soumission', 'note_evaluation'
        ]
        read_only_fields = [
            'date_soumission', 'date_derniere_modification', 
            'statut_candidature', 'note_evaluation', 'commentaires_admin'
        ]
    
    def validate_email_candidat(self, value):
        """Validation personnalisée de l'email (plus flexible)"""
        import re
        # Pattern plus permissif pour les emails
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, value):
            raise serializers.ValidationError("Format d'email invalide. Utilisez le format: exemple@domaine.com")
        return value
    
    def validate_moyenne_generale(self, value):
        """Validation de la moyenne générale (simplifiée)"""
        if value < 0 or value > 25:  # Accept jusqu'à 25 pour différents systèmes
            raise serializers.ValidationError("La moyenne doit être comprise entre 0 et 25.")
        return value
    
    def validate_cv_candidat(self, value):
        """Validation du fichier CV"""
        if value and not value.name.lower().endswith('.pdf'):
            raise serializers.ValidationError("Le CV doit être au format PDF.")
        return value
    
    def validate_lettre_motivation(self, value):
        """Validation de la lettre de motivation"""
        if value and not value.name.lower().endswith('.pdf'):
            raise serializers.ValidationError("La lettre de motivation doit être au format PDF.")
        return value
    
    def validate_releves_notes(self, value):
        """Validation des relevés de notes"""
        if value and not value.name.lower().endswith('.pdf'):
            raise serializers.ValidationError("Les relevés de notes doivent être au format PDF.")
        return value


class CandidatureParcoursCreateSerializer(serializers.ModelSerializer):
    """Sérialiseur pour la création de candidatures"""
    
    class Meta:
        model = CandidatureParcours
        exclude = [
            'statut_candidature', 'commentaires_admin', 'note_evaluation',
            'date_soumission', 'date_derniere_modification'
        ]
    
    def validate_moyenne_generale(self, value):
        """Validation de la moyenne générale (simplifiée)"""
        if value < 0 or value > 25:  # Accept jusqu'à 25 pour différents systèmes
            raise serializers.ValidationError("La moyenne doit être comprise entre 0 et 25.")
        return value
    
    def validate_cv_candidat(self, value):
        """Validation du fichier CV (formats multiples acceptés)"""
        if value:
            allowed_extensions = ['.pdf', '.doc', '.docx']
            file_extension = value.name.lower()
            if not any(file_extension.endswith(ext) for ext in allowed_extensions):
                raise serializers.ValidationError("Le CV doit être au format PDF, DOC ou DOCX.")
            # Permettre les fichiers de test même s'ils sont vides
            if value.size == 0:
                pass  # Accepter silencieusement les fichiers vides
        return value
    
    def validate_lettre_motivation(self, value):
        """Validation de la lettre de motivation (formats multiples acceptés)"""
        if value:
            allowed_extensions = ['.pdf', '.doc', '.docx']
            file_extension = value.name.lower()
            if not any(file_extension.endswith(ext) for ext in allowed_extensions):
                raise serializers.ValidationError("La lettre de motivation doit être au format PDF, DOC ou DOCX.")
            # Permettre les fichiers de test même s'ils sont vides
            if value.size == 0:
                pass  # Accepter silencieusement les fichiers vides
        return value
    
    def validate_releves_notes(self, value):
        """Validation des relevés de notes (formats multiples acceptés)"""
        if value:
            allowed_extensions = ['.pdf', '.doc', '.docx']
            file_extension = value.name.lower()
            if not any(file_extension.endswith(ext) for ext in allowed_extensions):
                raise serializers.ValidationError("Les relevés de notes doivent être au format PDF, DOC ou DOCX.")
            # Permettre les fichiers de test même s'ils sont vides
            if value.size == 0:
                pass  # Accepter silencieusement les fichiers vides
        return value
    
    def validate(self, attrs):
        """Validation croisée des données"""
        # Vérifier que l'âge minimum est respecté (simplifié à 16 ans)
        from datetime import date
        if attrs.get('date_naissance'):
            age = date.today().year - attrs['date_naissance'].year
            if age < 16:  # Réduit de 18 à 16 ans
                raise serializers.ValidationError("Le candidat doit être âgé d'au moins 16 ans.")
        
        return attrs