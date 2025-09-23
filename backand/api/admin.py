from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe

from .models import (
    Chercheur, ChercheurDiplome, Domaine, ChercheurDomaineExpertise,
    ChercheurMot, Poste, ChercheurPoste, ChercheurReseau,
    TypeLaboratoire, Laboratoire, ChercheurLaboratoire,
    LaboratoireDomaine, LaboratoireNew, LaboratoireParcour,
    LaboratoireParcourConditionAdmission, LaboratoireParcourDeboucher,
    LaboratoireParcourSpecialisation, Partenaire, LaboratoirePartenaire,
    LaboratoirePresentation, LaboratoirePresentationImage, LaboratoireMission,
    Page, LaboratoireSlider, Type, LaboratoireTypeNew, Recherche,
    RechercheChercheur, RecherchePhase, RechercheChronologie,
    RecherchePublication, RecherchePublicationCitation,
    RecherchePublicationMotCle, RechercheRealisation, RechercheLaboratoire,
    RechercheObjectif, RecherchePartenaire, CandidatureParcours,
    ContactLaboratoire, HoraireLaboratoire, MessageContact,
)

# Configuration des groupes d'administration
class AdminGroupConfig:
    """Configuration pour organiser l'interface d'administration"""
    
    # Définition des groupes et de leurs modèles
    GROUPS = {
        'Chercheurs et Personnel': {
            'models': ['Chercheur', 'ChercheurDiplome', 'ChercheurDomaineExpertise', 
                      'ChercheurMot', 'ChercheurPoste', 'ChercheurReseau'],
            'icon': '👨‍🔬'
        },
        'Laboratoires': {
            'models': ['Laboratoire', 'TypeLaboratoire', 'ChercheurLaboratoire',
                      'LaboratoireDomaine', 'LaboratoirePresentation', 
                      'LaboratoirePresentationImage', 'LaboratoireMission'],
            'icon': '🏢'
        },
        'Parcours et Formation': {
            'models': ['LaboratoireParcour', 'LaboratoireParcourConditionAdmission',
                      'LaboratoireParcourDeboucher', 'LaboratoireParcourSpecialisation',
                      'CandidatureParcours'],
            'icon': '🎓'
        },
        'Recherche et Publications': {
            'models': ['Recherche', 'RechercheChercheur', 'RecherchePhase',
                      'RechercheChronologie', 'RecherchePublication',
                      'RecherchePublicationCitation', 'RecherchePublicationMotCle',
                      'RechercheRealisation', 'RechercheLaboratoire', 'RechercheObjectif'],
            'icon': '📚'
        },
        'Partenariats': {
            'models': ['Partenaire', 'LaboratoirePartenaire', 'RecherchePartenaire'],
            'icon': '🤝'
        },
        'Configuration': {
            'models': ['Domaine', 'Poste', 'Page', 'Type'],
            'icon': '⚙️'
        }
    }

# Inlines pour regrouper les tables liées
class ChercheurDiplomeInline(admin.TabularInline):
    model = ChercheurDiplome
    extra = 1
    fields = ('etablissement', 'diplome', 'annee_obtention')

class ChercheurDomaineExpertiseInline(admin.TabularInline):
    model = ChercheurDomaineExpertise
    extra = 1
    fields = ('id_domaine',)

class ChercheurMotInline(admin.TabularInline):
    model = ChercheurMot
    extra = 1
    fields = ('titre', 'date')

class ChercheurPosteInline(admin.TabularInline):
    model = ChercheurPoste
    extra = 1
    fields = ('id_poste',)

class ChercheurReseauInline(admin.TabularInline):
    model = ChercheurReseau
    extra = 1
    fields = ('type_reseau', 'contact')

class LaboratoireParcourInline(admin.TabularInline):
    model = LaboratoireParcour
    extra = 0  # Pas de lignes vides par défaut
    fields = ('nom_parour', 'date_creation', 'duree_formation', 'nombre_etudiant_max', 'statu')
    classes = ['collapse']  # Section pliable

class LaboratoireParcourConditionAdmissionInline(admin.TabularInline):
    model = LaboratoireParcourConditionAdmission
    extra = 1
    fields = ('titre',)

class LaboratoireParcourDeboucherInline(admin.TabularInline):
    model = LaboratoireParcourDeboucher
    extra = 1
    fields = ('deboucher',)

class LaboratoireParcourSpecialisationInline(admin.TabularInline):
    model = LaboratoireParcourSpecialisation
    extra = 1
    fields = ('specialisation',)

class RechercheChercheurInline(admin.TabularInline):
    model = RechercheChercheur
    extra = 1
    fields = ('id_chercheur', 'role_equipe')

class RechercheChronologieInline(admin.TabularInline):
    model = RechercheChronologie
    extra = 1
    fields = ('id_recherche_phase', 'titre', 'etat')

class RecherchePublicationInline(admin.TabularInline):
    model = RecherchePublication
    extra = 1
    fields = ('titre', 'date_publication', 'fichier')

class RechercheObjectifInline(admin.TabularInline):
    model = RechercheObjectif
    extra = 1
    fields = ('objectif',)

class RechercheRealisationInline(admin.TabularInline):
    model = RechercheRealisation
    extra = 1
    fields = ('titre', 'date_realisation')

class RecherchePartenaireInline(admin.TabularInline):
    model = RecherchePartenaire
    extra = 1
    fields = ('id_partenaire', 'type_collaboration', 'date_debut')


@admin.register(Chercheur)
class ChercheurAdmin(admin.ModelAdmin):
    list_display = ('nom', 'prenom', 'statut', 'date_embauche', 'bureau')
    search_fields = ('nom', 'prenom')
    list_filter = ('statut',)
    inlines = [
        ChercheurDiplomeInline,
        ChercheurDomaineExpertiseInline,
        ChercheurMotInline,
        ChercheurPosteInline,
        ChercheurReseauInline
    ]
    
    fieldsets = (
        ('Informations personnelles', {
            'fields': ('nom', 'prenom')
        }),
        ('Informations professionnelles', {
            'fields': ('statut', 'date_embauche', 'bureau')
        }),
        ('Profil', {
            'fields': ('biographie', 'photo')
        })
    )

# Suppression des admins redondants maintenant gérés par les inlines
# @admin.register(ChercheurDiplome) - maintenant géré par ChercheurAdmin
# @admin.register(ChercheurDomaineExpertise) - maintenant géré par ChercheurAdmin
# @admin.register(ChercheurMot) - maintenant géré par ChercheurAdmin
# @admin.register(ChercheurPoste) - maintenant géré par ChercheurAdmin
# @admin.register(ChercheurReseau) - maintenant géré par ChercheurAdmin

@admin.register(Domaine)
class DomaineAdmin(admin.ModelAdmin):
    list_display = ('titre',)
    search_fields = ('titre',)

@admin.register(ChercheurDomaineExpertise)
class ChercheurDomaineExpertiseAdmin(admin.ModelAdmin):
    list_display = ('id_chercheur', 'id_domaine')
    search_fields = ('id_chercheur__nom', 'id_chercheur__prenom', 'id_domaine__titre')

@admin.register(ChercheurMot)
class ChercheurMotAdmin(admin.ModelAdmin):
    list_display = ('id_chercheur', 'titre', 'date')
    search_fields = ('id_chercheur__nom', 'id_chercheur__prenom', 'titre')

@admin.register(Poste)
class PosteAdmin(admin.ModelAdmin):
    list_display = ('nom', 'abreviation_poste', 'grade')
    search_fields = ('nom',)

@admin.register(ChercheurPoste)
class ChercheurPosteAdmin(admin.ModelAdmin):
    list_display = ('id_chercheur', 'id_poste')
    search_fields = ('id_chercheur__nom', 'id_chercheur__prenom', 'id_poste__nom')

@admin.register(ChercheurReseau)
class ChercheurReseauAdmin(admin.ModelAdmin):
    list_display = ('id_chercheur', 'type_reseau', 'contact')
    search_fields = ('id_chercheur__nom', 'id_chercheur__prenom', 'type_reseau')
    list_filter = ('type_reseau',)

@admin.register(TypeLaboratoire)
class TypeLaboratoireAdmin(admin.ModelAdmin):
    list_display = ('type_labo',)
    search_fields = ('type_labo',)

@admin.register(Laboratoire)
class LaboratoireAdmin(admin.ModelAdmin):
    list_display = ('nom', 'id_type_laboratoire', 'ufr', 'date_de_creation')
    search_fields = ('nom', 'ufr')
    inlines = [LaboratoireParcourInline]
    
    fieldsets = (
        ('Informations générales', {
            'fields': ('nom', 'id_type_laboratoire', 'ufr', 'date_de_creation')
        }),
        ('Média', {
            'fields': ('logo',)
        })
    )

@admin.register(ChercheurLaboratoire)
class ChercheurLaboratoireAdmin(admin.ModelAdmin):
    list_display = ('id_chercheur_poste', 'id_laboratoire', 'statu')
    search_fields = ('id_chercheur_poste__id_chercheur__nom', 'id_laboratoire__nom')
    list_filter = ('statu',)

@admin.register(LaboratoireDomaine)
class LaboratoireDomaineAdmin(admin.ModelAdmin):
    list_display = ('id_laboratoire', 'id_domaine')
    search_fields = ('id_laboratoire__nom', 'id_domaine__titre')

@admin.register(LaboratoireNew)
class LaboratoireNewAdmin(admin.ModelAdmin):
    list_display = ('id_laboratoire', 'titre', 'date_publication', 'statu')
    search_fields = ('titre',)
    list_filter = ('statu',)

@admin.register(LaboratoireParcour)
class LaboratoireParcourAdmin(admin.ModelAdmin):
    list_display = ('id_laboratoire', 'nom_parour', 'date_creation', 'statu')
    search_fields = ('nom_parour',)
    list_filter = ('statu',)
    inlines = [
        LaboratoireParcourConditionAdmissionInline,
        LaboratoireParcourDeboucherInline,
        LaboratoireParcourSpecialisationInline
    ]
    
    fieldsets = (
        ('Informations générales', {
            'fields': ('id_laboratoire', 'nom_parour', 'date_creation', 'statu')
        }),
        ('Description', {
            'fields': ('description',)
        }),
        ('Détails', {
            'fields': ('duree_formation', 'nombre_etudiant_max')
        })
    )

# Suppression des admins redondants maintenant gérés par LaboratoireParcourAdmin
# @admin.register(LaboratoireParcourConditionAdmission)
# @admin.register(LaboratoireParcourDeboucher)
# @admin.register(LaboratoireParcourSpecialisation)

@admin.register(Partenaire)
class PartenaireAdmin(admin.ModelAdmin):
    list_display = ('nom_partenaire', 'pays', 'ville', 'date_debut_partenariat')
    search_fields = ('nom_partenaire', 'pays', 'ville')

@admin.register(LaboratoirePartenaire)
class LaboratoirePartenaireAdmin(admin.ModelAdmin):
    list_display = ('id_laboratoire', 'id_partenaire', 'statu', 'type_partenaire')
    search_fields = ('id_laboratoire__nom', 'id_partenaire__nom_partenaire')
    list_filter = ('statu', 'type_partenaire')

@admin.register(LaboratoirePresentation)
class LaboratoirePresentationAdmin(admin.ModelAdmin):
    list_display = ('id_laboratoire', 'titre')
    search_fields = ('titre',)

@admin.register(LaboratoirePresentationImage)
class LaboratoirePresentationImageAdmin(admin.ModelAdmin):
    list_display = ('id_laboratoire',)

@admin.register(LaboratoireMission)
class LaboratoireMissionAdmin(admin.ModelAdmin):
    list_display = ('id_laboratoire', 'annee_creation', 'budget_annuel')

@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    list_display = ('titre',)
    search_fields = ('titre',)

@admin.register(LaboratoireSlider)
class LaboratoireSliderAdmin(admin.ModelAdmin):
    list_display = ('id_laboratoire', 'id_page', 'titre')
    search_fields = ('titre',)

@admin.register(Type)
class TypeAdmin(admin.ModelAdmin):
    list_display = ('type',)
    search_fields = ('type',)

@admin.register(LaboratoireTypeNew)
class LaboratoireTypeNewAdmin(admin.ModelAdmin):
    list_display = ('id_laboratoire_new', 'id_type')

@admin.register(Recherche)
class RechercheAdmin(admin.ModelAdmin):
    list_display = ('titre', 'statu', 'domaine_recherche', 'date_debut', 'date_fin_prevue', 'progression_temporelle_display')
    search_fields = ('titre', 'description', 'mots_cles')
    list_filter = ('statu', 'source_financement', 'domaine_recherche', 'date_debut')
    inlines = [
        RechercheChercheurInline,
        RechercheChronologieInline,
        RecherchePublicationInline,
        RechercheObjectifInline,
        RechercheRealisationInline,
        RecherchePartenaireInline
    ]
    
    fieldsets = (
        ('Informations générales', {
            'fields': ('titre', 'description', 'statu', 'domaine_recherche')
        }),
        ('Calendrier', {
            'fields': ('date_debut', 'date_fin_prevue', 'date_fin_reelle')
        }),
        ('Financement', {
            'fields': ('budget_total', 'source_financement')
        }),
        ('Métadonnées', {
            'fields': ('mots_cles',),
            'classes': ['collapse']
        })
    )
    
    readonly_fields = ('progression_temporelle_display', 'duree_prevue_display', 'duree_reelle_display')
    
    def progression_temporelle_display(self, obj):
        """Affiche la progression temporelle avec barre de progression"""
        progression = obj.progression_temporelle
        
        if progression == 0:
            couleur = '#6c757d'  # Gris
            statut = 'Non commencé'
        elif progression < 50:
            couleur = '#17a2b8'  # Bleu
            statut = 'En début'
        elif progression < 80:
            couleur = '#ffc107'  # Jaune
            statut = 'En cours'
        elif progression < 100:
            couleur = '#fd7e14'  # Orange
            statut = 'Bientôt fini'
        else:
            couleur = '#28a745'  # Vert
            statut = 'Terminé'
        
        return format_html(
            '<div style="width: 100px; background: #e9ecef; border-radius: 10px; overflow: hidden;">' +
            '<div style="width: {}%; background: {}; height: 20px; text-align: center; line-height: 20px; color: white; font-size: 11px; font-weight: bold;">' +
            '{}%</div></div>' +
            '<small style="color: {}; font-weight: bold;">{}</small>',
            progression, couleur, int(progression), couleur, statut
        )
    progression_temporelle_display.short_description = "Progression"
    
    def duree_prevue_display(self, obj):
        """Affiche la durée prévue de manière lisible"""
        duree = obj.duree_prevue
        if duree is not None:
            if duree < 30:
                return f"{duree} jours"
            elif duree < 365:
                mois = duree // 30
                jours = duree % 30
                return f"{mois} mois, {jours} jours"
            else:
                annees = duree // 365
                mois = (duree % 365) // 30
                return f"{annees} an(s), {mois} mois"
        return "Non définie"
    duree_prevue_display.short_description = "Durée prévue"
    
    def duree_reelle_display(self, obj):
        """Affiche la durée réelle de manière lisible"""
        duree = obj.duree_reelle
        if duree is not None:
            if duree < 30:
                return f"{duree} jours"
            elif duree < 365:
                mois = duree // 30
                jours = duree % 30
                return f"{mois} mois, {jours} jours"
            else:
                annees = duree // 365
                mois = (duree % 365) // 30
                return f"{annees} an(s), {mois} mois"
        return "Non terminée"
    duree_reelle_display.short_description = "Durée réelle"
    
    actions = ['marquer_en_cours', 'marquer_termine', 'exporter_recherches']
    
    def marquer_en_cours(self, request, queryset):
        """Action pour marquer les recherches comme en cours"""
        queryset.update(statu='En cours')
        self.message_user(request, f"{queryset.count()} recherche(s) marquée(s) comme en cours.")
    marquer_en_cours.short_description = "Marquer comme en cours"
    
    def marquer_termine(self, request, queryset):
        """Action pour marquer les recherches comme terminées"""
        from datetime import date
        queryset.update(statu='Terminer', date_fin_reelle=date.today())
        self.message_user(request, f"{queryset.count()} recherche(s) marquée(s) comme terminée(s).")
    marquer_termine.short_description = "Marquer comme terminé"
    
    def exporter_recherches(self, request, queryset):
        """Action pour exporter les recherches sélectionnées"""
        # Ici vous pourriez implémenter l'export CSV ou PDF
        self.message_user(request, f"Export de {queryset.count()} recherche(s) en préparation...")
    exporter_recherches.short_description = "Éxporter les recherches sélectionnées"

# Suppression des admins redondants maintenant gérés par RechercheAdmin
# @admin.register(RechercheChercheur)
# @admin.register(RechercheChronologie) 
# @admin.register(RechercheObjectif)
# @admin.register(RechercheRealisation)
# @admin.register(RecherchePartenaire)

@admin.register(RecherchePhase)
class RecherchePhaseAdmin(admin.ModelAdmin):
    list_display = ('phase',)
    search_fields = ('phase',)

@admin.register(RechercheChronologie)
class RechercheChronologieAdmin(admin.ModelAdmin):
    list_display = ('id_recherche', 'id_recherche_phase', 'titre', 'etat')
    search_fields = ('titre',)
    list_filter = ('etat',)

@admin.register(RecherchePublication)
class RecherchePublicationAdmin(admin.ModelAdmin):
    list_display = ('id_recherche', 'titre', 'date_publication', 'voir_fichier')
    search_fields = ('titre',)
    readonly_fields = ('fichier_link',)
    
    fieldsets = (
        ('Informations générales', {
            'fields': (
                'id_recherche',
                'titre',
                'resume',
                'date_publication'
            )
        }),
        ('Fichier et liens', {
            'fields': (
                'fichier',
                'fichier_link',
                'url_publication',
                'doi'
            )
        }),
        ('Métadonnées', {
            'fields': (
                'facteur_impact',
                'contenu'
            )
        })
    )
    
    def voir_fichier(self, obj):
        """Affiche un lien pour visualiser le fichier de publication"""
        if obj.fichier:
            return format_html(
                '<a href="{}" target="_blank" style="display:inline-block; padding:4px 8px; background:#dc3545; color:white; text-decoration:none; border-radius:3px; font-size:11px;">📄 Voir fichier</a>',
                obj.fichier.url
            )
        return "Pas de fichier"
    voir_fichier.short_description = "Fichier"
    
    def fichier_link(self, obj):
        """Lien pour télécharger/visualiser le fichier de publication"""
        if obj.fichier:
            return format_html(
                '<a href="{}" target="_blank" style="color: #dc3545; font-weight: bold;">📎 Télécharger le fichier</a><br><small style="color: #666;">{}</small>',
                obj.fichier.url,
                obj.fichier.name.split('/')[-1]
            )
        return "Aucun fichier attaché"
    fichier_link.short_description = "Lien du fichier"

@admin.register(RecherchePublicationCitation)
class RecherchePublicationCitationAdmin(admin.ModelAdmin):
    list_display = ('id_recherche_publication', 'citation')
    search_fields = ('citation',)

@admin.register(RecherchePublicationMotCle)
class RecherchePublicationMotCleAdmin(admin.ModelAdmin):
    list_display = ('id_recherche_publication', 'mot_cle')
    search_fields = ('mot_cle',)

@admin.register(RechercheRealisation)
class RechercheRealisationAdmin(admin.ModelAdmin):
    list_display = ('id_recherche', 'titre', 'date_realisation')
    search_fields = ('titre',)

@admin.register(RechercheLaboratoire)
class RechercheLaboratoireAdmin(admin.ModelAdmin):
    list_display = ('id_laboratoire_domaine', 'id_recherche')

@admin.register(RechercheObjectif)
class RechercheObjectifAdmin(admin.ModelAdmin):
    list_display = ('id_recherche', 'objectif')
    search_fields = ('objectif',)

@admin.register(RecherchePartenaire)
class RecherchePartenaireAdmin(admin.ModelAdmin):
    list_display = ('id_recherche', 'id_partenaire', 'type_collaboration', 'date_debut')
    search_fields = ('id_recherche__titre', 'id_partenaire__nom_partenaire')
    list_filter = ('type_collaboration',)


@admin.register(CandidatureParcours)
class CandidatureParcoursAdmin(admin.ModelAdmin):
    """Administration des candidatures aux parcours"""
    
    list_display = (
        'nom_complet', 'id_parcours', 'statut_candidature', 
        'date_soumission', 'note_evaluation', 'voir_documents'
    )
    
    list_filter = (
        'statut_candidature', 'niveau_etude_actuel',
        'id_parcours__id_laboratoire', 'date_soumission'
    )
    
    search_fields = (
        'nom_candidat', 'prenom_candidat', 'email_candidat',
        'id_parcours__nom_parour', 'etablissement_origine'
    )
    
    readonly_fields = (
        'date_soumission', 'date_derniere_modification', 'age',
        'cv_link', 'lettre_motivation_link', 'releves_notes_link', 'diplome_obtenu_link'
    )
    
    fieldsets = (
        ('Informations personnelles', {
            'fields': (
                ('nom_candidat', 'prenom_candidat'),
                ('date_naissance', 'lieu_naissance', 'nationalite'),
                'age'
            )
        }),
        ('Contact', {
            'fields': (
                ('telephone_candidat', 'email_candidat'),
                'adresse_complete',
                ('ville_residence', 'pays_residence')
            )
        }),
        ('Formation académique', {
            'fields': (
                'niveau_etude_actuel',
                'etablissement_origine',
                'filiere_etude',
                ('moyenne_generale', 'annee_obtention_diplome')
            )
        }),
        ('Documents', {
            'fields': (
                'cv_candidat', 'cv_link',
                'lettre_motivation', 'lettre_motivation_link',
                'releves_notes', 'releves_notes_link',
                'diplome_obtenu', 'diplome_obtenu_link'
            )
        }),
        ('Candidature', {
            'fields': (
                'id_parcours',
                # Champs motivation et projet supprimés
            )
        }),
        ('Évaluation', {
            'fields': (
                'statut_candidature',
                'note_evaluation',
                'commentaires_admin',
                ('date_soumission', 'date_derniere_modification')
            )
        })
    )
    
    def nom_complet(self, obj):
        """Affiche le nom complet du candidat"""
        return obj.nom_complet
    nom_complet.short_description = "Candidat"
    
    def voir_documents(self, obj):
        """Affiche des liens pour visualiser tous les documents"""
        html = '<div style="line-height: 1.5;">'
        
        if obj.cv_candidat:
            html += f'<a href="{obj.cv_candidat.url}" target="_blank" style="display:inline-block; margin:2px; padding:4px 8px; background:#007cba; color:white; text-decoration:none; border-radius:3px; font-size:11px;">CV</a>'
        
        if obj.lettre_motivation:
            html += f'<a href="{obj.lettre_motivation.url}" target="_blank" style="display:inline-block; margin:2px; padding:4px 8px; background:#28a745; color:white; text-decoration:none; border-radius:3px; font-size:11px;">Lettre</a>'
        
        if obj.releves_notes:
            html += f'<a href="{obj.releves_notes.url}" target="_blank" style="display:inline-block; margin:2px; padding:4px 8px; background:#ffc107; color:black; text-decoration:none; border-radius:3px; font-size:11px;">Notes</a>'
        
        if obj.diplome_obtenu:
            html += f'<a href="{obj.diplome_obtenu.url}" target="_blank" style="display:inline-block; margin:2px; padding:4px 8px; background:#6f42c1; color:white; text-decoration:none; border-radius:3px; font-size:11px;">Diplôme</a>'
        
        html += '</div>'
        return mark_safe(html) if any([obj.cv_candidat, obj.lettre_motivation, obj.releves_notes, obj.diplome_obtenu]) else "Aucun document"
    voir_documents.short_description = "Documents"
    
    def cv_link(self, obj):
        """Lien pour télécharger/visualiser le CV"""
        if obj.cv_candidat:
            return format_html(
                '<a href="{}" target="_blank" style="color: #007cba; font-weight: bold;">📎 Télécharger CV</a><br><small style="color: #666;">{}</small>',
                obj.cv_candidat.url,
                obj.cv_candidat.name.split('/')[-1]
            )
        return "Pas de CV"
    cv_link.short_description = "Lien CV"
    
    def lettre_motivation_link(self, obj):
        """Lien pour télécharger/visualiser la lettre de motivation"""
        if obj.lettre_motivation:
            return format_html(
                '<a href="{}" target="_blank" style="color: #28a745; font-weight: bold;">📎 Télécharger Lettre</a><br><small style="color: #666;">{}</small>',
                obj.lettre_motivation.url,
                obj.lettre_motivation.name.split('/')[-1]
            )
        return "Pas de lettre"
    lettre_motivation_link.short_description = "Lien Lettre de motivation"
    
    def releves_notes_link(self, obj):
        """Lien pour télécharger/visualiser les relevés de notes"""
        if obj.releves_notes:
            return format_html(
                '<a href="{}" target="_blank" style="color: #ffc107; font-weight: bold; color: #856404;">📎 Télécharger Notes</a><br><small style="color: #666;">{}</small>',
                obj.releves_notes.url,
                obj.releves_notes.name.split('/')[-1]
            )
        return "Pas de relevés"
    releves_notes_link.short_description = "Lien Relevés de notes"
    
    def diplome_obtenu_link(self, obj):
        """Lien pour télécharger/visualiser le diplôme"""
        if obj.diplome_obtenu:
            return format_html(
                '<a href="{}" target="_blank" style="color: #6f42c1; font-weight: bold;">📎 Télécharger Diplôme</a><br><small style="color: #666;">{}</small>',
                obj.diplome_obtenu.url,
                obj.diplome_obtenu.name.split('/')[-1]
            )
        return "Pas de diplôme"
    diplome_obtenu_link.short_description = "Lien Diplôme"


# ===================== ADMIN CONTACT =====================
@admin.register(ContactLaboratoire)
class ContactLaboratoireAdmin(admin.ModelAdmin):
    list_display = ('id_laboratoire', 'type_contact', 'ville', 'pays', 'telephone_principal', 'email_principal', 'est_actif')
    list_filter = ('type_contact', 'est_actif', 'pays', 'ville')
    search_fields = ('id_laboratoire__nom', 'ville', 'pays', 'nom_contact', 'adresse_complete', 'email_principal', 'telephone_principal')


@admin.register(HoraireLaboratoire)
class HoraireLaboratoireAdmin(admin.ModelAdmin):
    list_display = ('contact_laboratoire', 'jour_semaine', 'heure_ouverture', 'heure_fermeture', 'est_ferme')
    list_filter = ('jour_semaine', 'est_ferme')
    search_fields = ('contact_laboratoire__id_laboratoire__nom', 'notes')


@admin.register(MessageContact)
class MessageContactAdmin(admin.ModelAdmin):
    list_display = ('nom_complet_expediteur', 'id_laboratoire', 'email_expediteur', 'sujet_message', 'priorite', 'statut_message', 'est_traite', 'date_envoi')
    list_filter = ('priorite', 'statut_message', 'est_traite', 'date_envoi')
    search_fields = ('prenom_expediteur', 'nom_expediteur', 'email_expediteur', 'sujet_message', 'contenu_message')

    def save_model(self, request, obj, form, change):
        """
        À l'enregistrement d'une réponse admin, envoie l'email à l'expéditeur
        si un contenu de réponse est présent.
        """
        super().save_model(request, obj, form, change)

        # Envoyer la réponse admin si le champ est rempli
        try:
            from .services import EmailService

            a_une_reponse = bool(obj.reponse_admin and obj.reponse_admin.strip())
            if a_une_reponse:
                EmailService.envoyer_reponse_admin(obj)
        except Exception:
            # On évite de bloquer l'admin en cas d'erreur; les logs capteront le détail
            pass


# Configuration de l'interface d'administration
admin.site.site_header = "Administration UNA - Gestion Laboratoires"
admin.site.site_title = "Admin UNA"
admin.site.index_title = "Interface d'Administration - Université Numérique Africaine"

# Personnalisation des groupes dans l'admin
class AdminConfig:
    """Configuration personnalisée de l'admin pour regroupement logique"""
    
    # Configuration des groupes d'applications
    APP_GROUPS = {
        "Gestion des Chercheurs": [
            "Chercheur", "Domaine", "Poste"
        ],
        "Gestion des Laboratoires": [
            "Laboratoire", "TypeLaboratoire", "LaboratoireParcour"
        ],
        "Gestion de la Recherche": [
            "Recherche", "RecherchePhase", "RecherchePublication"
        ],
        "Candidatures et Formations": [
            "CandidatureParcours"
        ],
        "Partenariats": [
            "Partenaire"
        ],
        "Configuration Système": [
            "Page", "Type"
        ]
    }
