from django.db import models


class Chercheur(models.Model):
    STATUT_CHOICES = [
        ("actif", "Actif"),
        ("inactif", "Inactif"),
        ("retraite", "Retraité"),
        ("depart", "Départ"),
    ]
    nom = models.CharField(max_length=255, null=True, blank=True)
    prenom = models.CharField(max_length=255, null=True, blank=True)
    biographie = models.TextField(null=True, blank=True)
    photo = models.ImageField(upload_to="static/photoTeam/", null=True, blank=True)
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default="actif")
    date_embauche = models.DateField()
    bureau = models.CharField(max_length=255)
    creer_le = models.DateTimeField(auto_now_add=True)
    mise_a_jour_le = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f"{self.prenom} {self.nom}"


class ChercheurDiplome(models.Model):
    id_chercheur = models.ForeignKey(Chercheur, on_delete=models.CASCADE)
    etablissement = models.CharField(max_length=255)
    diplome = models.CharField(max_length=255)
    annee_obtention = models.DateField()
    creer_le = models.DateTimeField(auto_now_add=True)
    mise_a_jour_le = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.id_chercheur.prenom} {self.id_chercheur.nom} - {self.etablissement}"


class Domaine(models.Model):
    titre = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to="static/images/")
    creer_le = models.DateTimeField(auto_now_add=True)
    mise_a_jour_le = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.titre


class ChercheurDomaineExpertise(models.Model):
    id_chercheur = models.ForeignKey(Chercheur, on_delete=models.CASCADE)
    id_domaine = models.ForeignKey(Domaine, on_delete=models.CASCADE)
    creer_le = models.DateTimeField(auto_now_add=True)
    mise_a_jour_le = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.id_chercheur.prenom} {self.id_chercheur.nom} - {self.id_domaine.titre}"


class ChercheurMot(models.Model):
    id_chercheur = models.ForeignKey(Chercheur, on_delete=models.CASCADE)
    titre = models.CharField(max_length=255)
    mot = models.TextField()
    date = models.DateField()
    creer_le = models.DateTimeField(auto_now_add=True)
    mise_a_jour_le = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.id_chercheur.prenom} {self.id_chercheur.nom} - {self.titre}"


class Poste(models.Model):
    nom = models.CharField(max_length=255)
    abreviation_poste = models.CharField(max_length=255)
    grade = models.CharField(max_length=255, null=True, blank=True)
    creer_le = models.DateTimeField(auto_now_add=True)
    mise_a_jour_le = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nom


class ChercheurPoste(models.Model):
    id_chercheur = models.ForeignKey(Chercheur, on_delete= models.CASCADE)
    id_poste = models.ForeignKey(Poste, on_delete= models.CASCADE)
    creer_le = models.DateTimeField(auto_now_add=True)
    mise_a_jour_le = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.id_chercheur.prenom} {self.id_chercheur.nom} - {self.id_poste.nom}"


class ChercheurReseau(models.Model):
    TYPE_RESEAU = [
        ("Facebook", "Facebook"),
        ("Twitter", "Twitter"),
        ("LinkedIn", "LinkedIn"),
        ("Instagram", "Instagram"),
        ("YouTube", "YouTube"),
        ("TikTok", "TikTok"),
        ("WhatsApp", "WhatsApp"),
        ("Telegram", "Telegram"),
        ("Snapchat", "Snapchat"),
        ("ResearchGate", "ResearchGate"),
        ("ORCID", "ORCID"),
        ("GoogleScholar", "GoogleScholar"),
        ("GitHub", "GitHub"),
        ("SiteWeb", "SiteWeb"),
        ("Email", "Email"),
        ("Téléphone", "Téléphone"),
    ]
        
    id_chercheur = models.ForeignKey(Chercheur, on_delete=models.CASCADE)
    type_reseau = models.CharField(max_length=50, choices=TYPE_RESEAU)
    contact = models.CharField(max_length=255)
    creer_le = models.DateTimeField(auto_now_add=True)
    mise_a_jour_le = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "ChercheurReseau"
        verbose_name_plural = "ChercheurReseaux"

    def __str__(self):
        return f"{self.id_chercheur.prenom} {self.id_chercheur.nom} - {self.type_reseau}"


class TypeLaboratoire(models.Model):
    type_labo = models.CharField(max_length=255)
    creer_le = models.DateTimeField(auto_now_add=True)
    mise_a_jour_le = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.type_labo


class Laboratoire(models.Model):
    id_type_laboratoire = models.ForeignKey(TypeLaboratoire, on_delete=models.CASCADE)
    nom = models.CharField(max_length=255)
    logo = models.ImageField(upload_to="static/images/")
    ufr = models.CharField(max_length=255)
    date_de_creation = models.DateField()
    creer_le = models.DateTimeField(auto_now_add=True)
    mise_a_jour_le = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nom


class ChercheurLaboratoire(models.Model):
    id_chercheur_poste = models.ForeignKey(ChercheurPoste, on_delete=models.CASCADE)
    id_laboratoire = models.ForeignKey(Laboratoire, on_delete=models.CASCADE)
    statu = models.CharField(max_length=20, choices=[("Actif", "Actif"), ("Inactif", "Inactif")], default="Actif")
    creer_le = models.DateTimeField(auto_now_add=True)
    mise_a_jour_le = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.id_chercheur_poste.id_chercheur.prenom} {self.id_chercheur_poste.id_chercheur.nom} - {self.id_laboratoire.nom}"


class LaboratoireDomaine(models.Model):
    id_laboratoire = models.ForeignKey(Laboratoire, on_delete=models.CASCADE)
    id_domaine = models.ForeignKey(Domaine , on_delete = models.CASCADE)
    creer_le = models.DateTimeField(auto_now_add=True)
    mise_a_jour_le = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{} - {}".format(self.id_laboratoire.nom, self.id_domaine.titre)
    

class LaboratoireNew(models.Model):
    STATUT_CHOICES = [
        ("Actif", "Actif"),
        ("Inactif", "Inactif"),

    ]
    id_laboratoire = models.ForeignKey(Laboratoire, on_delete=models.CASCADE)
    titre = models.CharField(max_length=100)
    extrait = models.CharField(max_length=100)
    phrase_cle = models.CharField(max_length=150)
    contenu_complet = models.TextField()
    date_publication = models.DateField()
    image_principal = models.ImageField(upload_to="static/images/")
    statu = models.CharField(choices=STATUT_CHOICES, max_length=90, default="Actif")
    creer_le = models.DateTimeField(auto_now_add=True)
    mise_a_jour_le = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.titre
    

class LaboratoireParcour(models.Model):
    STATUT_CHOICES = [
        ("Actif", "Actif"),
        ("Inactif", "Inactif"),

    ]
    id_laboratoire = models.ForeignKey(Laboratoire, on_delete=models.CASCADE)
    nom_parour = models.CharField(max_length=255)
    date_creation = models.DateField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    duree_formation = models.IntegerField(null=True, blank=True)
    nombre_etudiant_max = models.IntegerField(null=True, blank=True)
    statu = models.CharField(choices=STATUT_CHOICES, max_length=90, default="Actif")
    creer_le = models.DateTimeField(auto_now_add=True)
    mise_a_jour_le = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nom_parour


class LaboratoireParcourConditionAdmission(models.Model):
    id_laboratoire_parcour = models.ForeignKey(LaboratoireParcour, on_delete=models.CASCADE)
    titre = models.CharField(max_length=255)
    valeur = models.CharField(max_length=255, null=True)
    creer_le = models.DateTimeField(auto_now_add=True)
    mise_a_jour_le = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.titre
    

class LaboratoireParcourDeboucher(models.Model):
    id_laboratoire_parcour = models.ForeignKey(LaboratoireParcour, on_delete=models.CASCADE)
    deboucher = models.CharField(max_length=255)
    creer_le = models.DateTimeField(auto_now_add=True)
    mise_a_jour_le = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.id_laboratoire_parcour.id_laboratoire.nom} - {self.deboucher}"
        

class LaboratoireParcourSpecialisation(models.Model):
    id_laboratoire_parcour = models.ForeignKey(LaboratoireParcour, on_delete=models.CASCADE)
    specialisation = models.CharField(max_length=255)
    creer_le = models.DateTimeField(auto_now_add=True)
    mise_a_jour_le = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.id_laboratoire_parcour.id_laboratoire.nom} - {self.specialisation}"


class Partenaire(models.Model):
    logo = models.ImageField(upload_to="static/logoPartenaire/")
    nom_partenaire = models.CharField(max_length=200)
    pays = models.CharField(max_length=100, null=True, blank=True)
    ville = models.CharField(max_length=100, null=True, blank=True)
    adresse = models.TextField(null=True, blank=True)
    site_web = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    telephone = models.CharField(max_length=20, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    date_debut_partenariat = models.DateField(null=True, blank=True)
    date_fin_partenariat = models.DateField(null=True, blank=True)
    notes = models.TextField(null=True, blank=True)
    creer_le = models.DateTimeField(auto_now_add=True)
    mise_a_jour_le = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nom_partenaire


class LaboratoirePartenaire(models.Model):
    STATUT_CHOICES = [
        ("Actif", "Actif"),
        ("Inactif", "Inactif"),
        ("Termine", "Terminé"),
    ]

    Partenaire_CHOICES = [
        ("Académiques et scientifiques", "Académiques et scientifiques"),
        ("Institutionnels", "Institutionnels"),
        ("Industriels et privés", "Industriels et privés"),
        ("Financiers", "Financiers"),
        ("Technologiques et d’innovation", "Technologiques et d’innovation"),
        ("Associatifs et société civile", "Associatifs et société civile"),
    ]

    id_laboratoire = models.ForeignKey(Laboratoire, on_delete=models.CASCADE)
    id_partenaire = models.ForeignKey(Partenaire, on_delete=models.CASCADE)
    statu = models.CharField(max_length=20, choices=STATUT_CHOICES, default="Actif")
    type_partenaire = models.CharField(max_length=100, choices=Partenaire_CHOICES)
    creer_le = models.DateTimeField(auto_now_add=True)
    mise_a_jour_le = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.id_laboratoire.nom} - {self.id_partenaire.nom_partenaire}"


class LaboratoirePresentation(models.Model):
    id_laboratoire = models.ForeignKey(Laboratoire, on_delete=models.CASCADE)
    titre = models.CharField(max_length=255)
    description = models.TextField()
    creer_le = models.DateTimeField(auto_now_add=True)
    mise_a_jour_le = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{} - {}".format(self.id_laboratoire.nom, self.titre)


class LaboratoirePresentationImage(models.Model):
    id_laboratoire = models.ForeignKey(Laboratoire, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="static/imagePresentation/")
    creer_le = models.DateTimeField(auto_now_add=True)
    mise_a_jour_le = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.id_laboratoire.nom


class LaboratoireMission(models.Model):
    id_laboratoire = models.ForeignKey(Laboratoire, on_delete=models.CASCADE)
    description = models.TextField()
    annee_creation = models.DateField()
    budget_annuel = models.BigIntegerField()
    monnaie = models.CharField(max_length=20, default='FCFA')
    creer_le = models.DateTimeField(auto_now_add=True)
    mise_a_jour_le = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.id_laboratoire.nom


class Page(models.Model):
    titre = models.CharField(max_length=255)
    creer_le = models.DateTimeField(auto_now_add=True)
    mise_a_jour_le = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.titre


class LaboratoireSlider(models.Model):
    id_laboratoire = models.ForeignKey(Laboratoire, on_delete=models.CASCADE)
    id_page = models.ForeignKey(Page, on_delete=models.CASCADE)
    titre = models.CharField(max_length=255)
    description = models.TextField()
    creer_le = models.DateTimeField(auto_now_add=True)
    mise_a_jour_le = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.id_page.titre} - {self.titre}"


class Type(models.Model):
    type = models.CharField(max_length=100)
    creer_le = models.DateTimeField(auto_now_add=True)
    mise_a_jour_le = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.type


class LaboratoireTypeNew(models.Model):
    id_laboratoire_new = models.ForeignKey(LaboratoireNew, on_delete=models.CASCADE)
    id_type = models.ForeignKey(Type, on_delete=models.CASCADE)
    creer_le = models.DateTimeField(auto_now_add=True)
    mise_a_jour_le = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{} - {}".format(self.id_laboratoire_new.id_laboratoire.nom, self.id_type.type)


class Recherche(models.Model):
    STATUT_CHOICES = [
        ("Planifier", "Planifiér"),
        ("En cours", "En cours"),
        ("Terminer", "Terminer"),
        ("Suspendu", "Suspendu"),
        ("Annuler", "Annuler"),
    ]
    titre = models.CharField(max_length=255)
    description = models.TextField()
    statu = models.CharField(max_length=20, choices=STATUT_CHOICES, default="Planifier")
    date_debut = models.DateField()
    date_fin_prevue = models.DateField(null=True, blank=True)
    date_fin_reelle = models.DateField(null=True, blank=True)
    budget_total = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    creer_le = models.DateTimeField(auto_now_add=True)
    mise_a_jour_le = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.titre


class RechercheChercheur(models.Model):
    ROLE_CHOICES = [
        ("chef_projet", "Chef de projet"),
        ("chercheur_principal", "Chercheur principal"),
        ("chercheur_associe", "Chercheur associé"),
        ("post_doc", "Post-doc"),
        ("etudiant", "Étudiant"),
    ]
    id_recherche = models.ForeignKey(Recherche, on_delete=models.CASCADE)
    id_chercheur = models.ForeignKey(Chercheur, on_delete=models.CASCADE)
    role_equipe = models.CharField(max_length=30, choices=ROLE_CHOICES)
    creer_le = models.DateTimeField(auto_now_add=True)
    mise_a_jour_le = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.id_recherche.titre} - {self.id_chercheur.prenom} {self.id_chercheur.nom}"


class RecherchePhase(models.Model):
    phase = models.CharField(max_length=255, default="phase 1")
    creer_le = models.DateTimeField(auto_now_add=True)
    mise_a_jour_le = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.phase


class RechercheChronologie(models.Model):
    ETAT_CHOICES = [("en cours", "En cours"), ("termine", "Terminé"), ("en attente", "En attente")]
    id_recherche = models.ForeignKey(Recherche, on_delete=models.CASCADE)
    id_recherche_phase = models.ForeignKey(RecherchePhase, on_delete=models.CASCADE)
    titre = models.CharField(max_length=255)
    date_debut = models.DateField()
    date_fin = models.DateField()
    etat = models.CharField(max_length=20, choices=ETAT_CHOICES)
    creer_le = models.DateTimeField(auto_now_add=True)
    mise_a_jour_le = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.id_recherche.titre} - {self.id_recherche_phase.phase}"


class RecherchePublication(models.Model):
    id_recherche = models.ForeignKey(Recherche, on_delete=models.CASCADE)
    titre = models.CharField(max_length=255)
    resume = models.TextField(null=True, blank=True)
    fichier = models.FileField(upload_to="static/documentsPublication/")
    doi = models.CharField(max_length=200, null=True, blank=True)
    facteur_impact = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    date_publication = models.DateField(null=True, blank=True)
    url_publication = models.CharField(max_length=255, null=True, blank=True)
    contenu = models.TextField()
    creer_le = models.DateTimeField(auto_now_add=True)
    mise_a_jour_le = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.titre


class RecherchePublicationCitation(models.Model):
    id_recherche_publication = models.ForeignKey(RecherchePublication, on_delete=models.CASCADE)
    citation = models.CharField(max_length=255)
    creer_le = models.DateTimeField(auto_now_add=True)
    mise_a_jour_le = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.citation


class RecherchePublicationMotCle(models.Model):
    id_recherche_publication = models.ForeignKey(RecherchePublication, on_delete=models.CASCADE)
    mot_cle = models.CharField(max_length=255)
    creer_le = models.DateTimeField(auto_now_add=True)
    mise_a_jour_le = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.mot_cle


class RechercheRealisation(models.Model):
    id_recherche = models.ForeignKey(Recherche, on_delete=models.CASCADE)
    titre = models.CharField(max_length=255)
    description = models.TextField()
    date_realisation = models.DateField()
    impact = models.CharField(max_length=255)
    lien_externe = models.URLField()
    creer_le = models.DateTimeField(auto_now_add=True)
    mise_a_jour_le = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.titre


class RechercheLaboratoire(models.Model):
    id_laboratoire_domaine = models.ForeignKey(LaboratoireDomaine, on_delete=models.CASCADE)
    id_recherche = models.ForeignKey(Recherche, on_delete=models.CASCADE)
    creer_le = models.DateTimeField(auto_now_add=True)
    mise_a_jour_le = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.id_laboratoire_domaine.id_laboratoire.nom} - {self.id_recherche.titre} - {self.id_laboratoire_domaine.id_domaine.titre}"


class RechercheObjectif(models.Model):
    id_recherche = models.ForeignKey(Recherche, on_delete=models.CASCADE)
    objectif = models.CharField(max_length=255)
    creer_le = models.DateTimeField(auto_now_add=True)
    mise_a_jour_le = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.id_recherche.titre} - {self.objectif}"
    

class RecherchePartenaire(models.Model):
    CHOICE = [
        ("Financement" , 'Financement'),
        ('Ressources' , "Ressources"),
        ('Expertise' , 'Expertise'),
        ('Equipements', 'Equipements'),
        ('Personnel' , 'Personnel'),
    ]

    id_recherche = models.ForeignKey(Recherche, on_delete=models.CASCADE)
    id_partenaire = models.ForeignKey(Partenaire, on_delete=models.CASCADE)
    type_collaboration = models.CharField(max_length=255, choices=CHOICE)
    contribution_partenaire = models.CharField(max_length=255, null=True)
    contribution_laboratoire = models.CharField(max_length=255, null=True)
    date_debut = models.DateField()
    date_fin = models.DateField()
    montant_financement = models.BigIntegerField()
    monnaie = models.CharField(max_length=20, default="FCFA")
    creer_le = models.DateTimeField(auto_now_add=True)
    mise_a_jour_le = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.id_recherche.titre} - {self.id_partenaire.nom_partenaire}"


class CandidatureParcours(models.Model):
    """
    Modèle pour les candidatures aux parcours de laboratoire
    """
    STATUT_CANDIDATURE_CHOICES = [
        ("En attente", "En attente de traitement"),
        ("En cours d'examen", "En cours d'examen"),
        ("Acceptée", "Candidature acceptée"),
        ("Refusée", "Candidature refusée"),
        ("Liste d'attente", "En liste d'attente"),
    ]
    
    NIVEAU_ETUDE_CHOICES = [
        ("Licence", "Licence (Bac+3)"),
        ("Master 1", "Master 1 (Bac+4)"),
        ("Master 2", "Master 2 (Bac+5)"),
        ("Doctorat", "Doctorat (Bac+8)"),
        ("Autre", "Autre niveau"),
    ]
    
    MOTIVATION_CHOICES = [
        ("Recherche académique", "Intérêt pour la recherche académique"),
        ("Application industrielle", "Application dans l'industrie"),
        ("Développement personnel", "Développement des compétences personnelles"),
        ("Innovation technologique", "Contribution à l'innovation technologique"),
        ("Impact social", "Créer un impact social positif"),
    ]

    # Informations personnelles
    nom_candidat = models.CharField(max_length=255, verbose_name="Nom de famille")
    prenom_candidat = models.CharField(max_length=255, verbose_name="Prénom")
    date_naissance = models.DateField(verbose_name="Date de naissance")
    lieu_naissance = models.CharField(max_length=255, verbose_name="Lieu de naissance")
    nationalite = models.CharField(max_length=100, verbose_name="Nationalité")
    
    # Informations de contact
    telephone_candidat = models.CharField(max_length=20, verbose_name="Numéro de téléphone")
    email_candidat = models.EmailField(verbose_name="Adresse email")
    adresse_complete = models.TextField(verbose_name="Adresse complète")
    ville_residence = models.CharField(max_length=255, verbose_name="Ville de résidence")
    pays_residence = models.CharField(max_length=100, verbose_name="Pays de résidence")
    
    # Informations académiques
    niveau_etude_actuel = models.CharField(
        max_length=50, 
        choices=NIVEAU_ETUDE_CHOICES, 
        verbose_name="Niveau d'étude actuel"
    )
    etablissement_origine = models.CharField(max_length=255, verbose_name="Établissement d'origine")
    filiere_etude = models.CharField(max_length=255, verbose_name="Filière d'étude")
    moyenne_generale = models.DecimalField(
        max_digits=4, 
        decimal_places=2, 
        verbose_name="Moyenne générale (/20)"
    )
    annee_obtention_diplome = models.PositiveIntegerField(verbose_name="Année d'obtention du diplôme")
    
    # Documents joints
    cv_candidat = models.FileField(
        upload_to="static/candidatures/cv/", 
        verbose_name="Curriculum Vitae (PDF)"
    )
    lettre_motivation = models.FileField(
        upload_to="static/candidatures/lettres/", 
        verbose_name="Lettre de motivation (PDF)"
    )
    releves_notes = models.FileField(
        upload_to="static/candidatures/notes/", 
        verbose_name="Relevés de notes (PDF)"
    )
    diplome_obtenu = models.FileField(
        upload_to="static/candidatures/diplomes/", 
        verbose_name="Copie du diplôme (PDF)",
        null=True, blank=True
    )
    
    # Informations spécifiques à la candidature
    id_parcours = models.ForeignKey(
        LaboratoireParcour, 
        on_delete=models.CASCADE, 
        verbose_name="Parcours demandé"
    )
    motivation_principale = models.TextField(null=True, blank=True)
    projet_professionnel = models.TextField(null=True, blank=True)
    attentes_formation = models.TextField(null=True, blank=True)
    
    # Statut et suivi
    statut_candidature = models.CharField(
        max_length=50,
        choices=STATUT_CANDIDATURE_CHOICES,
        default="En attente",
        verbose_name="Statut de la candidature"
    )
    date_soumission = models.DateTimeField(auto_now_add=True, verbose_name="Date de soumission")
    date_derniere_modification = models.DateTimeField(auto_now=True, verbose_name="Dernière modification")
    
    # Commentaires administratifs
    commentaires_admin = models.TextField(
        verbose_name="Commentaires administratifs",
        help_text="Commentaires internes pour le suivi de la candidature",
        null=True, blank=True
    )
    note_evaluation = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        verbose_name="Note d'évaluation (/20)",
        null=True, blank=True
    )
    
    class Meta:
        verbose_name = "Candidature au parcours"
        verbose_name_plural = "Candidatures aux parcours"
        ordering = ['-date_soumission']
    
    def __str__(self):
        return f"{self.prenom_candidat} {self.nom_candidat} - {self.id_parcours.nom_parour}"
    
    @property
    def nom_complet(self):
        """Retourne le nom complet du candidat"""
        return f"{self.prenom_candidat} {self.nom_candidat}"
    
    @property
    def age(self):
        """Calcule l'âge du candidat"""
        from datetime import date
        today = date.today()
        return today.year - self.date_naissance.year - (
            (today.month, today.day) < (self.date_naissance.month, self.date_naissance.day)
        )
