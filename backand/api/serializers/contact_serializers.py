from rest_framework import serializers
from api.models import ContactLaboratoire, HoraireLaboratoire, MessageContact


class HoraireLaboratoireSerializer(serializers.ModelSerializer):
    jour_semaine_display = serializers.CharField(source='get_jour_semaine_display', read_only=True)

    class Meta:
        model = HoraireLaboratoire
        fields = [
            'id', 'jour_semaine', 'jour_semaine_display',
            'heure_ouverture', 'heure_fermeture', 'est_ferme', 'notes',
            'creer_le', 'mise_a_jour_le'
        ]


class ContactLaboratoireListSerializer(serializers.ModelSerializer):
    laboratoire_nom = serializers.CharField(source='id_laboratoire.nom', read_only=True)
    type_contact_display = serializers.CharField(source='get_type_contact_display', read_only=True)

    class Meta:
        model = ContactLaboratoire
        fields = [
            'id', 'laboratoire_nom', 'type_contact', 'type_contact_display',
            'ville', 'code_postal', 'pays', 'adresse_complete',
            'telephone_principal', 'email_principal',
            'est_actif'
        ]


class ContactLaboratoireSerializer(serializers.ModelSerializer):
    laboratoire_nom = serializers.CharField(source='id_laboratoire.nom', read_only=True)
    type_contact_display = serializers.CharField(source='get_type_contact_display', read_only=True)
    horaires = HoraireLaboratoireSerializer(many=True, source='horairelaboratoire_set', read_only=True)

    class Meta:
        model = ContactLaboratoire
        fields = [
            'id', 'id_laboratoire', 'laboratoire_nom', 'type_contact', 'type_contact_display',
            'adresse_complete', 'ville', 'code_postal', 'pays',
            'telephone_principal', 'email_principal',
            'site_web',
            'est_actif', 'horaires', 'creer_le', 'mise_a_jour_le'
        ]


class ContactLaboratoireCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactLaboratoire
        fields = [
            'id_laboratoire', 'type_contact', 'adresse_complete', 'ville', 'code_postal', 'pays',
            'telephone_principal', 'email_principal',
            'site_web', 'est_actif'
        ]


class HoraireLaboratoireCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = HoraireLaboratoire
        fields = [
            'contact_laboratoire', 'jour_semaine', 'heure_ouverture', 'heure_fermeture', 'est_ferme', 'notes'
        ]


class MessageContactListSerializer(serializers.ModelSerializer):
    laboratoire_nom = serializers.CharField(source='id_laboratoire.nom', read_only=True)
    priorite_display = serializers.CharField(source='get_priorite_display', read_only=True)
    statut_message_display = serializers.CharField(source='get_statut_message_display', read_only=True)
    nom_complet_expediteur = serializers.ReadOnlyField()

    class Meta:
        model = MessageContact
        fields = [
            'id', 'laboratoire_nom', 'nom_complet_expediteur', 'email_expediteur',
            'sujet_message', 'statut_message_display', 'priorite_display', 'est_traite', 'date_envoi'
        ]


class MessageContactSerializer(serializers.ModelSerializer):
    laboratoire_nom = serializers.CharField(source='id_laboratoire.nom', read_only=True)
    priorite_display = serializers.CharField(source='get_priorite_display', read_only=True)
    statut_message_display = serializers.CharField(source='get_statut_message_display', read_only=True)
    nom_complet_expediteur = serializers.ReadOnlyField()

    class Meta:
        model = MessageContact
        fields = [
            'id', 'id_laboratoire', 'laboratoire_nom', 'prenom_expediteur', 'nom_expediteur',
            'nom_complet_expediteur', 'email_expediteur', 'organisation_expediteur',
            'sujet_message', 'contenu_message', 'statut_message', 'statut_message_display',
            'priorite', 'priorite_display', 'reponse_admin', 'responsable_reponse', 'date_reponse',
            'est_traite', 'date_envoi', 'date_derniere_modification'
        ]


class MessageContactCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = MessageContact
        fields = [
            'id_laboratoire', 'prenom_expediteur', 'nom_expediteur', 'email_expediteur',
            'organisation_expediteur', 'sujet_message', 'contenu_message', 'priorite'
        ]
