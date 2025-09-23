"""
Services pour la gestion des emails et autres fonctionnalités
"""
from django.core.mail import send_mail, get_connection, EmailMultiAlternatives
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from api.models import Laboratoire
import logging

logger = logging.getLogger(__name__)


class EmailService:
    """
    Service pour gérer l'envoi d'emails
    """
    
    @staticmethod
    def envoyer_notification_nouveau_message(message_contact):
        """
        Envoie une notification par email lorsqu'un nouveau message de contact est reçu
        
        Args:
            message_contact: Instance du modèle MessageContact
        """
        try:
            # Utiliser toujours le laboratoire avec ID=1 si disponible
            try:
                laboratoire = Laboratoire.objects.get(pk=1)
            except Laboratoire.DoesNotExist:
                laboratoire = message_contact.id_laboratoire
            
            # Chercher l'email principal du laboratoire
            contact_principal = laboratoire.contactlaboratoire_set.filter(
                type_contact='principal',
                est_actif=True
            ).first()

            # Déterminer le destinataire et les identifiants SMTP
            if not contact_principal or not contact_principal.email_principal:
                return False
            
            # Préparer le contenu de l'email
            sujet = f"[{laboratoire.nom}] Nouveau message de contact - {message_contact.sujet_message}"
            
            # Contenu HTML de l'email
            contenu_html = f"""
            <html>
            <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                    <h2 style="color: #2c5aa0; border-bottom: 2px solid #2c5aa0; padding-bottom: 10px;">
                        Nouveau Message de Contact
                    </h2>
                    
                    <div style="background-color: #f8f9fa; padding: 15px; border-radius: 5px; margin: 20px 0;">
                        <h3 style="margin-top: 0; color: #495057;">Détails de l'expéditeur :</h3>
                        <p><strong>Nom :</strong> {message_contact.nom_complet_expediteur}</p>
                        <p><strong>Email :</strong> {message_contact.email_expediteur}</p>
                        {f'<p><strong>Organisation :</strong> {message_contact.organisation_expediteur}</p>' if message_contact.organisation_expediteur else ''}
                        <p><strong>Priorité :</strong> {message_contact.get_priorite_display()}</p>
                    </div>
                    
                    <div style="margin: 20px 0;">
                        <h3 style="color: #495057;">Sujet :</h3>
                        <p style="font-weight: bold; font-size: 16px;">{message_contact.sujet_message}</p>
                    </div>
                    
                    <div style="margin: 20px 0;">
                        <h3 style="color: #495057;">Message :</h3>
                        <div style="background-color: #ffffff; padding: 15px; border-left: 4px solid #2c5aa0; border-radius: 3px;">
                            {message_contact.contenu_message.replace(chr(10), '<br>')}
                        </div>
                    </div>
                    
                    <div style="margin-top: 30px; padding-top: 20px; border-top: 1px solid #dee2e6; color: #6c757d; font-size: 12px;">
                        <p>Ce message a été envoyé le {message_contact.date_envoi.strftime('%d/%m/%Y à %H:%M')} via le formulaire de contact du site web.</p>
                        <p>Pour répondre à ce message, utilisez l'adresse email : {message_contact.email_expediteur}</p>
                    </div>
                </div>
            </body>
            </html>
            """
            
            # Contenu texte brut (fallback)
            contenu_texte = f"""
Nouveau Message de Contact - {laboratoire.nom}

Détails de l'expéditeur :
- Nom : {message_contact.nom_complet_expediteur}
- Email : {message_contact.email_expediteur}
{f'- Organisation : {message_contact.organisation_expediteur}' if message_contact.organisation_expediteur else ''}
- Priorité : {message_contact.get_priorite_display()}

Sujet : {message_contact.sujet_message}

Message :
{message_contact.contenu_message}

---
Ce message a été envoyé le {message_contact.date_envoi.strftime('%d/%m/%Y à %H:%M')} via le formulaire de contact du site web.
Pour répondre à ce message, utilisez l'adresse email : {message_contact.email_expediteur}
            """
            
            # Déterminer les identifiants SMTP depuis la base (obligatoires pour l'envoi)
            smtp_username = contact_principal.email_principal
            smtp_password = getattr(contact_principal, 'mot_de_passe_email', None)
            if not smtp_username or not smtp_password:
                return False
            # L'expéditeur doit correspondre au compte authentifié (Gmail)
            from_email = smtp_username

            # Connexion SMTP personnalisée (fallback sur settings si manquant)
            connection = get_connection(
                host=settings.EMAIL_HOST,
                port=settings.EMAIL_PORT,
                username=smtp_username,
                password=smtp_password,
                use_tls=getattr(settings, 'EMAIL_USE_TLS', True),
                fail_silently=False,
            )

            # Envoyer l'email en multipart (texte + HTML)
            email = EmailMultiAlternatives(
                subject=sujet,
                body=contenu_texte,
                from_email=from_email,
                to=[contact_principal.email_principal],
                connection=connection,
            )
            email.attach_alternative(contenu_html, "text/html")
            resultat = email.send()
            
            return resultat > 0
                
        except Exception:
            return False
    
    @staticmethod
    def envoyer_confirmation_expediteur(message_contact):
        """
        Envoie un email de confirmation à l'expéditeur du message
        
        Args:
            message_contact: Instance du modèle MessageContact
        """
        try:
            # Utiliser toujours le laboratoire avec ID=1 si disponible
            try:
                laboratoire = Laboratoire.objects.get(pk=1)
            except Laboratoire.DoesNotExist:
                laboratoire = message_contact.id_laboratoire
            
            # Préparer le contenu de l'email de confirmation
            sujet = f"Confirmation de réception - {message_contact.sujet_message}"
            
            contenu_html = f"""
            <html>
            <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                    <h2 style="color: #2c5aa0; border-bottom: 2px solid #2c5aa0; padding-bottom: 10px;">
                        Confirmation de Réception
                    </h2>
                    
                    <p>Bonjour {message_contact.prenom_expediteur},</p>
                    
                    <p>Nous avons bien reçu votre message adressé au <strong>{laboratoire.nom}</strong>.</p>
                    
                    <div style="background-color: #f8f9fa; padding: 15px; border-radius: 5px; margin: 20px 0;">
                        <h3 style="margin-top: 0; color: #495057;">Récapitulatif de votre message :</h3>
                        <p><strong>Sujet :</strong> {message_contact.sujet_message}</p>
                        <p><strong>Date d'envoi :</strong> {message_contact.date_envoi.strftime('%d/%m/%Y à %H:%M')}</p>
                        <p><strong>Priorité :</strong> {message_contact.get_priorite_display()}</p>
                    </div>
                    
                    <p>Notre équipe prendra connaissance de votre demande dans les plus brefs délais. Nous vous répondrons généralement sous 48 heures ouvrables.</p>
                    
                    <p>Si votre demande est urgente, n'hésitez pas à nous contacter directement par téléphone.</p>
                    
                    <div style="margin-top: 30px; padding-top: 20px; border-top: 1px solid #dee2e6; color: #6c757d; font-size: 12px;">
                        <p>Cordialement,<br>L'équipe du {laboratoire.nom}</p>
                        <p>Ceci est un message automatique, merci de ne pas y répondre.</p>
                    </div>
                </div>
            </body>
            </html>
            """
            
            contenu_texte = f"""
Confirmation de Réception

Bonjour {message_contact.prenom_expediteur},

Nous avons bien reçu votre message adressé au {laboratoire.nom}.

Récapitulatif de votre message :
- Sujet : {message_contact.sujet_message}
- Date d'envoi : {message_contact.date_envoi.strftime('%d/%m/%Y à %H:%M')}
- Priorité : {message_contact.get_priorite_display()}

Notre équipe prendra connaissance de votre demande dans les plus brefs délais. Nous vous répondrons généralement sous 48 heures ouvrables.

Si votre demande est urgente, n'hésitez pas à nous contacter directement par téléphone.

Cordialement,
L'équipe du {laboratoire.nom}

Ceci est un message automatique, merci de ne pas y répondre.
            """
            
            # Déterminer le contact principal pour les identifiants SMTP
            contact_principal = laboratoire.contactlaboratoire_set.filter(
                type_contact='principal',
                est_actif=True
            ).first()

            # Nécessite des identifiants valides en BD; sinon on ne tente pas l'envoi
            smtp_username = contact_principal.email_principal if contact_principal else None
            smtp_password = getattr(contact_principal, 'mot_de_passe_email', None) if contact_principal else None
            if not smtp_username or not smtp_password:
                return False
            from_email = smtp_username

            connection = get_connection(
                host=settings.EMAIL_HOST,
                port=settings.EMAIL_PORT,
                username=smtp_username,
                password=smtp_password,
                use_tls=getattr(settings, 'EMAIL_USE_TLS', True),
                fail_silently=False,
            )

            email = EmailMultiAlternatives(
                subject=sujet,
                body=contenu_texte,
                from_email=from_email,
                to=[message_contact.email_expediteur],
                connection=connection,
            )
            email.attach_alternative(contenu_html, "text/html")
            resultat = email.send()
            
            return resultat > 0
                
        except Exception:
            return False

    @staticmethod
    def envoyer_reponse_admin(message_contact):
        """
        Envoie la réponse de l'administrateur à l'expéditeur du message
        """
        try:
            # Utiliser toujours le laboratoire avec ID=1 si disponible
            try:
                laboratoire = Laboratoire.objects.get(pk=1)
            except Laboratoire.DoesNotExist:
                laboratoire = message_contact.id_laboratoire

            if not message_contact.reponse_admin:
                return False

            sujet = f"Réponse à votre message - {message_contact.sujet_message}"

            contenu_html = f"""
            <html>
            <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                    <h2 style="color: #2c5aa0; border-bottom: 2px solid #2c5aa0; padding-bottom: 10px;">
                        Réponse du laboratoire
                    </h2>
                    <p>Bonjour {message_contact.prenom_expediteur},</p>
                    <p>Suite à votre message adressé au <strong>{laboratoire.nom}</strong>, voici notre réponse :</p>
                    <div style="background-color: #ffffff; padding: 15px; border-left: 4px solid #2c5aa0; border-radius: 3px; white-space: pre-wrap;">
                        {message_contact.reponse_admin.replace(chr(10), '<br>')}
                    </div>
                    {f'<p style="margin-top:16px"><strong>Responsable :</strong> {message_contact.responsable_reponse}</p>' if message_contact.responsable_reponse else ''}
                    <div style="margin-top: 30px; padding-top: 20px; border-top: 1px solid #dee2e6; color: #6c757d; font-size: 12px;">
                        <p>Cordialement,<br>L'équipe du {laboratoire.nom}</p>
                        <p>Merci de répondre directement à cet email si besoin.</p>
                    </div>
                </div>
            </body>
            </html>
            """

            contenu_texte = f"""
Réponse du laboratoire

Bonjour {message_contact.prenom_expediteur},

Suite à votre message adressé au {laboratoire.nom}, voici notre réponse :

{message_contact.reponse_admin}

{f'Responsable: {message_contact.responsable_reponse}' if message_contact.responsable_reponse else ''}

Cordialement,
L'équipe du {laboratoire.nom}
            """

            # Identifiants SMTP depuis le contact principal
            contact_principal = laboratoire.contactlaboratoire_set.filter(
                type_contact='principal',
                est_actif=True
            ).first()

            smtp_username = contact_principal.email_principal if contact_principal else None
            smtp_password = getattr(contact_principal, 'mot_de_passe_email', None) if contact_principal else None
            if not smtp_username or not smtp_password:
                return False

            connection = get_connection(
                host=settings.EMAIL_HOST,
                port=settings.EMAIL_PORT,
                username=smtp_username,
                password=smtp_password,
                use_tls=getattr(settings, 'EMAIL_USE_TLS', True),
                fail_silently=False,
            )

            email = EmailMultiAlternatives(
                subject=sujet,
                body=contenu_texte,
                from_email=smtp_username,
                to=[message_contact.email_expediteur],
                connection=connection,
            )
            email.attach_alternative(contenu_html, "text/html")
            resultat = email.send()

            return resultat > 0

        except Exception:
            return False