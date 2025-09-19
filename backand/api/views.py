from django.shortcuts import render
import re
from rest_framework import viewsets, filters, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import (
    Chercheur, LaboratoireParcour, CandidatureParcours, Laboratoire,
    RecherchePublication, RecherchePublicationMotCle, RecherchePublicationCitation,
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


class ChercheurViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Vue pour afficher les chercheurs
    """
    queryset = Chercheur.objects.filter(statut='actif')
    permission_classes = [AllowAny]
    filter_backends = [filters.SearchFilter]
    search_fields = ['nom', 'prenom']
    
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
        Filtrage optionnel par laboratoire
        """
        queryset = super().get_queryset()
        
        # Filtre par ID de laboratoire
        laboratoire_id = self.request.query_params.get('laboratoire_id', None)
        if laboratoire_id is not None:
            try:
                queryset = queryset.filter(id_laboratoire=laboratoire_id)
            except ValueError:
                pass  # Ignore les valeurs non numériques
        
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
