# 📧 Système d'Email Automatique pour les Contacts UNA Lab

## 🚀 Fonctionnalités Implémentées

Le système d'email automatique a été entièrement intégré et fonctionne comme suit :

### 1. **Envoi Automatique d'Emails**
Lorsqu'une personne soumet un message via le formulaire de contact :
- ✅ **Email de notification** envoyé au laboratoire concerné
- ✅ **Email de confirmation** envoyé à l'expéditeur

### 2. **Configuration Gmail SMTP**
- **Serveur SMTP** : smtp.gmail.com
- **Port** : 587 (TLS)
- **Email** : houessoueros3@gmail.com
- **Authentification** : Mot de passe d'application Gmail

## 📁 Fichiers Modifiés

### Backend (Django)
1. **`backand/settings.py`** - Configuration email et logging
2. **`api/services.py`** - Service d'envoi d'emails (nouveau)
3. **`api/views.py`** - Intégration du service email
4. **`test_email.py`** - Script de test de base
5. **`test_contact_email.py`** - Script de test complet

### Frontend (React)
- Les hooks et services existants fonctionnent déjà parfaitement
- Aucune modification nécessaire côté frontend

## 🔧 Configuration Gmail

### Prérequis
1. **Authentification à 2 facteurs activée** sur le compte Gmail
2. **Mot de passe d'application généré** (déjà configuré)

### Générer un nouveau mot de passe d'application
Si besoin de changer le mot de passe :
1. Aller sur [myaccount.google.com](https://myaccount.google.com)
2. Sécurité → Authentification à 2 facteurs
3. Mots de passe d'application
4. Générer un nouveau mot de passe
5. Remplacer dans `settings.py`

## 🧪 Tests

### Test Simple
```bash
cd backand
python test_email.py
```

### Test Complet (avec création de message)
```bash
cd backand
python test_contact_email.py
```

## 📧 Format des Emails

### Email de Notification (au laboratoire)
```
Sujet: [Nom du Laboratoire] Nouveau message de contact - Sujet du message

Contenu:
- Détails de l'expéditeur (nom, email, organisation)
- Priorité du message
- Sujet et contenu complet
- Date d'envoi
- Instructions pour répondre
```

### Email de Confirmation (à l'expéditeur)
```
Sujet: Confirmation de réception - Sujet du message

Contenu:
- Confirmation de réception
- Récapitulatif du message envoyé
- Délai de réponse estimé (48h)
- Coordonnées du laboratoire
```

## 🔄 Flux Complet

1. **Utilisateur** remplit le formulaire de contact sur le site
2. **Frontend** envoie les données à l'API Django
3. **API Django** sauvegarde le message en base de données
4. **Service Email** envoie automatiquement :
   - Notification au laboratoire
   - Confirmation à l'expéditeur
5. **Logs** enregistrent le succès/échec des envois

## 🛠️ Maintenance

### Logs
Les logs sont stockés dans : `backand/logs/django.log`

### Surveillance
- Vérifier régulièrement les logs pour les erreurs d'envoi
- Surveiller le quota Gmail (limite quotidienne)
- Tester périodiquement avec `test_email.py`

## 🔐 Sécurité

- ✅ Mot de passe d'application Gmail utilisé
- ✅ Données sensibles masquées dans les logs
- ✅ Gestion d'erreur sans interruption du service
- ✅ Validation des données côté frontend et backend

## 📱 Interface Utilisateur

Le formulaire de contact fonctionne déjà parfaitement :
- Validation en temps réel
- Messages d'erreur/succès
- Indicateur de chargement
- Fallback mailto si l'API est indisponible

## ✅ Statut : **OPÉRATIONNEL**

Le système d'email automatique est entièrement fonctionnel et prêt à l'utilisation !

---

*Dernière mise à jour : 22 septembre 2025*