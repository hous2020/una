from django.shortcuts import render
import re
from rest_framework import viewsets, filters, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import (
    Chercheur, LaboratoireParcour, CandidatureParcours, Laboratoire,
    RecherchePublication, RecherchePublicationMotCle, RecherchePublicationCitation, ChercheurLaboratoire, ChercheurPoste, RechercheLaboratoire, RechercheChercheur,
    ContactLaboratoire, HoraireLaboratoire, MessageContact,
)
from .serializers.chercheur_serializers import ChercheurSerializer, ChercheurListSerializer
from .serializers.laboratoire_serializers import (
    LaboratoireParcourSerializer, LaboratoireParcourListSerializer,
    CandidatureParcoursSerializer, CandidatureParcoursCreateSerializer,
    LaboratoireSerializer
)
from .serializers.publication_serializers import (
    RecherchePublicationListSerializer,
    RecherchePublicationDetailSerializer,
)
from .serializers.contact_serializers import (
    ContactLaboratoireSerializer,
    ContactLaboratoireListSerializer,
    ContactLaboratoireCreateSerializer,
    HoraireLaboratoireSerializer,
    HoraireLaboratoireCreateSerializer,
    MessageContactSerializer,
    MessageContactListSerializer,
    MessageContactCreateSerializer,
)
from .services import EmailService
import logging

logger = logging.getLogger(__name__)


class ChercheurViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Vue pour afficher les chercheurs
    """
    queryset = Chercheur.objects.filter(statut='actif')
    permission_classes = [AllowAny]
    filter_backends = [filters.SearchFilter]
    search_fields = ['nom', 'prenom']

    def get_queryset(self):
        """
        Surcharge de la méthode pour filtrer les chercheurs par laboratoire.
        """
        queryset = super().get_queryset()
        laboratoire_id = self.request.query_params.get('laboratoire_id')

        if laboratoire_id:
            try:
                # Récupérer les ID des ChercheurPoste liés au laboratoire
                chercheur_poste_ids = ChercheurLaboratoire.objects.filter(
                    id_laboratoire_id=laboratoire_id
                ).values_list('id_chercheur_poste_id', flat=True)

                # Récupérer les ID des Chercheurs liés à ces ChercheurPoste
                chercheur_ids = ChercheurPoste.objects.filter(
                    id__in=chercheur_poste_ids
                ).values_list('id_chercheur_id', flat=True)

                # Filtrer le queryset des chercheurs
                queryset = queryset.filter(id__in=chercheur_ids)

            except (ValueError, TypeError):
                # En cas d'ID de laboratoire invalide, ne rien faire
                pass

        return queryset
    
    def get_serializer_class(self):
        """
        Retourne le sérialiseur approprié selon l'action
        """
        if self.action == 'list':
            return ChercheurListSerializer
        return ChercheurSerializer
    
    def get_serializer_context(self):
        """
        Ajoute la requête au contexte du sérialiseur
        """
        context = super().get_serializer_context()
        context.update({'request': self.request})
        return context


class LaboratoireViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Vue pour afficher les laboratoires
    """
    queryset = Laboratoire.objects.all()
    permission_classes = [AllowAny]
    serializer_class = LaboratoireSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['nom', 'ufr', 'id_type_laboratoire__type_labo']
    
    def get_serializer_context(self):
        """
        Ajoute la requête au contexte du sérialiseur
        """
        context = super().get_serializer_context()
        context.update({'request': self.request})
        return context
    
    @action(detail=True, methods=['get'])
    def parcours(self, request, pk=None):
        """
        Retourne les parcours d'un laboratoire spécifique
        """
        try:
            laboratoire = self.get_object()
            parcours = LaboratoireParcour.objects.filter(
                id_laboratoire=laboratoire,
                statu='Actif'
            )
            serializer = LaboratoireParcourListSerializer(
                parcours, 
                many=True, 
                context={'request': request}
            )
            return Response(serializer.data)
        except Exception as e:
            return Response(
                {'error': f'Erreur lors de la récupération des parcours: {str(e)}'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class LaboratoireParcourViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Vue pour afficher les parcours de laboratoire
    """
    queryset = LaboratoireParcour.objects.filter(statu='Actif')
    permission_classes = [AllowAny]
    filter_backends = [filters.SearchFilter]
    search_fields = ['nom_parour', 'description', 'id_laboratoire__nom', 'id_laboratoire__ufr']
    
    def get_serializer_class(self):
        """
        Retourne le sérialiseur approprié selon l'action
        """
        if self.action == 'list':
            return LaboratoireParcourListSerializer
        return LaboratoireParcourSerializer
    
    def get_serializer_context(self):
        """
        Ajoute la requête au contexte du sérialiseur
        """
        context = super().get_serializer_context()
        context.update({'request': self.request})
        return context
    
    def get_queryset(self):
        """
        Filtrage par laboratoire avec ID 1 par défaut
        """
        queryset = super().get_queryset()
        
        # Filtre par ID de laboratoire (par défaut: laboratoire ID 1)
        laboratoire_id = self.request.query_params.get('laboratoire_id', '1')
        try:
            queryset = queryset.filter(id_laboratoire=laboratoire_id)
        except ValueError:
            # Si la valeur n'est pas valide, on utilise quand même l'ID 1 par défaut
            queryset = queryset.filter(id_laboratoire=1)
        
        # Filtre par nom de laboratoire
        laboratoire_nom = self.request.query_params.get('laboratoire_nom', None)
        if laboratoire_nom is not None:
            queryset = queryset.filter(id_laboratoire__nom__icontains=laboratoire_nom)
        
        return queryset.order_by('-date_creation')


class CandidatureParcoursViewSet(viewsets.ModelViewSet):
    """
    Vue pour gerer les candidatures aux parcours
    """
    queryset = CandidatureParcours.objects.all()
    permission_classes = [AllowAny]
    filter_backends = [filters.SearchFilter]
    search_fields = ['nom_candidat', 'prenom_candidat', 'email_candidat', 'id_parcours__nom_parour']
    
    def get_serializer_class(self):
        """
        Retourne le serialiseur approprie selon l'action
        """
        if self.action == 'create':
            return CandidatureParcoursCreateSerializer
        return CandidatureParcoursSerializer
    
    def get_queryset(self):
        """
        Filtrage optionnel par parcours
        """
        queryset = super().get_queryset()
        parcours_id = self.request.query_params.get('parcours', None)
        if parcours_id is not None:
            queryset = queryset.filter(id_parcours=parcours_id)
        return queryset.order_by('-date_soumission')
    
    def create(self, request, *args, **kwargs):
        """
        Creation d'une nouvelle candidature
        """
        # Verification de base
        has_data = hasattr(request, 'data') and request.data
        has_files = hasattr(request, 'FILES') and request.FILES
        
        if not has_data:
            return Response({
                'error': 'Aucune donnee recue'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Tentative de serialisation
        try:
            serializer = self.get_serializer(data=request.data)
            is_valid = serializer.is_valid()
            
            if not is_valid:
                return Response({
                    'error': 'Donnees invalides',
                    'details': serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:
            return Response({
                'error': f'Erreur de serialisation: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        # Verification des doublons
        try:
            email = serializer.validated_data.get('email_candidat')
            parcours = serializer.validated_data.get('id_parcours')
            
            if email and parcours:
                existing = CandidatureParcours.objects.filter(
                    email_candidat=email,
                    id_parcours=parcours
                ).first()
                
                if existing:
                    return Response(
                        {'error': 'Une candidature existe deja pour ce parcours avec cette adresse email.'},
                        status=status.HTTP_400_BAD_REQUEST
                    )
        except Exception as e:
            pass  # Continue si erreur de verification
        
        # Sauvegarde
        try:
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            
            return Response(
                {
                    'message': 'Candidature soumise avec succes!',
                    'candidature': serializer.data
                },
                status=status.HTTP_201_CREATED,
                headers=headers
            )
            
        except Exception as e:
            return Response(
                {
                    'error': f'Erreur lors de la sauvegarde: {str(e)}',
                    'type': type(e).__name__
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class RecherchePublicationViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Vue pour consulter les publications de recherche avec capacités de recherche
    et de filtrage par mots-clés et citations.
    """
    queryset = RecherchePublication.objects.all()
    permission_classes = [AllowAny]
    filter_backends = [filters.SearchFilter]
    search_fields = ['titre', 'resume', 'contenu', 'doi', 'url_publication', 'id_recherche__titre']

    def get_serializer_class(self):
        if self.action == 'list':
            return RecherchePublicationListSerializer
        return RecherchePublicationDetailSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({'request': self.request})
        return context

    def get_queryset(self):
        qs = super().get_queryset()

        # Filtre par mot-clé (un ou plusieurs séparés par des virgules)
        mot_cle_param = self.request.query_params.get('mot_cle')
        if mot_cle_param:
            mots = [m.strip() for m in mot_cle_param.split(',') if m.strip()]
            if mots:
                pattern = '|'.join([re.escape(m) for m in mots])
                pub_ids = RecherchePublicationMotCle.objects.filter(
                    mot_cle__iregex=pattern
                ).values_list('id_recherche_publication_id', flat=True)
                qs = qs.filter(id__in=pub_ids)

        # Filtre par citation (texte contenu dans une citation liée)
        citation_param = self.request.query_params.get('citation')
        if citation_param:
            pub_ids = RecherchePublicationCitation.objects.filter(
                citation__icontains=citation_param
            ).values_list('id_recherche_publication_id', flat=True)
            qs = qs.filter(id__in=pub_ids)

        # Filtre par année de publication
        year = self.request.query_params.get('year')
        if year and year.isdigit():
            qs = qs.filter(date_publication__year=int(year))

        # Filtre par facteur d'impact minimal
        min_fi = self.request.query_params.get('min_facteur_impact')
        try:
            if min_fi is not None:
                qs = qs.filter(facteur_impact__gte=float(min_fi))
        except ValueError:
            pass

        # Filtre par id de recherche
        recherche_id = self.request.query_params.get('recherche')
        if recherche_id and recherche_id.isdigit():
            qs = qs.filter(id_recherche_id=int(recherche_id))

        # Filtre par laboratoire (par défaut: laboratoire ID 1)
        laboratoire_id = self.request.query_params.get('laboratoire_id', '1')
        try:
            lab_id_int = int(laboratoire_id)
        except ValueError:
            lab_id_int = 1  # Valeur par défaut si conversion échoue
            
        # Filtre par domaine de laboratoire
        laboratoire_domaine_id = self.request.query_params.get('laboratoire_domaine_id')
        
        # Utilisation prioritaire de RechercheLaboratoire pour le filtrage
        recherche_filter = RechercheLaboratoire.objects.filter(
            id_laboratoire_domaine__id_laboratoire_id=lab_id_int
        )
        
        # Ajouter le filtre de domaine si spécifié
        if laboratoire_domaine_id and laboratoire_domaine_id.isdigit():
            recherche_filter = recherche_filter.filter(
                id_laboratoire_domaine_id=int(laboratoire_domaine_id)
            )
            
        # Obtenir les IDs de recherche depuis RechercheLaboratoire
        recherche_ids = recherche_filter.values_list('id_recherche_id', flat=True)
        
        # Filtrer les publications par les recherches trouvées
        qs = qs.filter(id_recherche_id__in=recherche_ids)

        # Présence de fichier PDF
        has_pdf = self.request.query_params.get('has_pdf')
        if has_pdf in ['1', 'true', 'True']:
            qs = qs.exclude(fichier='')

        # Présence d'URL publique
        has_url = self.request.query_params.get('has_url')
        if has_url in ['1', 'true', 'True']:
            qs = qs.exclude(url_publication__isnull=True).exclude(url_publication='')

        # Tri (par défaut: plus récentes d'abord)
        ordering = self.request.query_params.get('ordering', '-date_publication')
        try:
            qs = qs.order_by(ordering)
        except Exception:
            qs = qs.order_by('-date_publication')

        return qs


class ContactLaboratoireViewSet(viewsets.ModelViewSet):
    """
    API contacts du laboratoire
    """
    queryset = ContactLaboratoire.objects.all()
    permission_classes = [AllowAny]
    filter_backends = [filters.SearchFilter]
    search_fields = ['id_laboratoire__nom', 'ville', 'pays', 'nom_contact', 'adresse_complete']

    def get_serializer_class(self):
        if self.action in ['list']:
            return ContactLaboratoireListSerializer
        if self.action in ['create']:
            return ContactLaboratoireCreateSerializer
        return ContactLaboratoireSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        laboratoire_id = self.request.query_params.get('laboratoire_id')
        type_contact = self.request.query_params.get('type_contact')
        if laboratoire_id and laboratoire_id.isdigit():
            qs = qs.filter(id_laboratoire_id=int(laboratoire_id))
        if type_contact:
            qs = qs.filter(type_contact=type_contact)
        return qs.order_by('-est_actif', 'type_contact')

    def get_serializer_context(self):
        ctx = super().get_serializer_context()
        ctx.update({'request': self.request})
        return ctx

    @action(detail=True, methods=['get'])
    def horaires(self, request, pk=None):
        contact = self.get_object()
        horaires = HoraireLaboratoire.objects.filter(contact_laboratoire=contact)
        ser = HoraireLaboratoireSerializer(horaires, many=True, context={'request': request})
        return Response(ser.data)


class HoraireLaboratoireViewSet(viewsets.ModelViewSet):
    """
    API horaires du laboratoire
    """
    queryset = HoraireLaboratoire.objects.all()
    permission_classes = [AllowAny]
    filter_backends = [filters.SearchFilter]
    search_fields = ['notes', 'contact_laboratoire__id_laboratoire__nom']

    def get_serializer_class(self):
        if self.action in ['create']:
            return HoraireLaboratoireCreateSerializer
        return HoraireLaboratoireSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        
        # Récupérer les paramètres de requête
        contact_id = self.request.query_params.get('contact_id')
        jour = self.request.query_params.get('jour')
        ouvert_seulement = self.request.query_params.get('ouvert_seulement')
        laboratoire_id = self.request.query_params.get('laboratoire_id', '1')  # Par défaut laboratoire ID 1
        
        # Filtrer par contact_id si spécifié
        if contact_id and contact_id.isdigit():
            qs = qs.filter(contact_laboratoire_id=int(contact_id))
        else:
            # Si contact_id n'est pas spécifié, filtrer par laboratoire_id
            try:
                lab_id = int(laboratoire_id)
                # Filtrer les horaires des contacts associés au laboratoire spécifié
                qs = qs.filter(contact_laboratoire__id_laboratoire_id=lab_id)
            except ValueError:
                # En cas d'erreur, utiliser laboratoire ID 1 par défaut
                qs = qs.filter(contact_laboratoire__id_laboratoire_id=1)
                
        # Autres filtres existants
        if jour and jour.isdigit():
            qs = qs.filter(jour_semaine=int(jour))
        if ouvert_seulement in ['1', 'true', 'True']:
            qs = qs.filter(est_ferme=False)
        return qs.order_by('jour_semaine')

    def get_serializer_context(self):
        ctx = super().get_serializer_context()
        ctx.update({'request': self.request})
        return ctx


class MessageContactViewSet(viewsets.ModelViewSet):
    """
    API messages de contact
    """
    queryset = MessageContact.objects.all()
    permission_classes = [AllowAny]
    filter_backends = [filters.SearchFilter]
    search_fields = ['prenom_expediteur', 'nom_expediteur', 'email_expediteur', 'sujet_message', 'contenu_message']

    def get_serializer_class(self):
        if self.action in ['list']:
            return MessageContactListSerializer
        if self.action in ['create']:
            return MessageContactCreateSerializer
        return MessageContactSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        laboratoire_id = self.request.query_params.get('laboratoire_id')
        statut = self.request.query_params.get('statut')
        priorite = self.request.query_params.get('priorite')
        traite = self.request.query_params.get('traite')
        date_debut = self.request.query_params.get('date_debut')
        date_fin = self.request.query_params.get('date_fin')

        if laboratoire_id and laboratoire_id.isdigit():
            qs = qs.filter(id_laboratoire_id=int(laboratoire_id))
        if statut:
            qs = qs.filter(statut_message=statut)
        if priorite:
            qs = qs.filter(priorite=priorite)
        if traite in ['1', 'true', 'True']:
            qs = qs.filter(est_traite=True)
        if date_debut:
            qs = qs.filter(date_envoi__date__gte=date_debut)
        if date_fin:
            qs = qs.filter(date_envoi__date__lte=date_fin)
        return qs.order_by('-date_envoi')

    def get_serializer_context(self):
        ctx = super().get_serializer_context()
        ctx.update({'request': self.request})
        return ctx
    
    def perform_create(self, serializer):
        """Surcharge pour envoyer les emails après création du message"""
        # Sauvegarder le message
        message = serializer.save()
        
        # Envoyer les notifications par email
        try:
            # Email de notification au laboratoire
            notif_ok = EmailService.envoyer_notification_nouveau_message(message)
            if notif_ok:
                logger.info(f"Notification envoyée au laboratoire pour le message {message.id}")
            else:
                logger.warning(f"Notification NON envoyée (config manquante) pour le message {message.id}")
            
            # Email de confirmation à l'expéditeur
            conf_ok = EmailService.envoyer_confirmation_expediteur(message)
            if conf_ok:
                logger.info(f"Confirmation envoyée à l'expéditeur pour le message {message.id}")
            else:
                logger.warning(f"Confirmation NON envoyée (config manquante) pour le message {message.id}")
            
        except Exception as e:
            logger.error(f"Erreur lors de l'envoi des emails pour le message {message.id}: {str(e)}")
            # Ne pas faire échouer la création du message si l'email échoue
        
        return message

    @action(detail=True, methods=['patch'])
    def marquer_traite(self, request, pk=None):
        message = self.get_object()
        message.est_traite = True
        message.statut_message = 'traite'
        message.reponse_admin = request.data.get('reponse_admin', message.reponse_admin)
        message.responsable_reponse = request.data.get('responsable_reponse', message.responsable_reponse)
        message.save(update_fields=['est_traite', 'statut_message', 'reponse_admin', 'responsable_reponse'])
        ser = MessageContactSerializer(message, context={'request': request})
        return Response(ser.data)
