from django import forms
from django.contrib.postgres.forms import SimpleArrayField

class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "Identifiant", "class": "form-control"}))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={"placeholder": "Mot de passe", "class": "form-control"}))


class formulaire_forgot_password(forms.Form):
    email = forms.CharField(max_length=80)


class formulaire_reset_password(forms.Form):
    email = forms.CharField(max_length=32)


BASE_CHOICES = (("interne", "interne"), ("externe", "externe"))


class PartnerForm(forms.Form):
    bases = forms.MultipleChoiceField(choices=BASE_CHOICES, required=False)
    nom_contact = forms.CharField(widget=forms.TextInput(
        attrs={"placeholder": "Nom", "class": "form-control"}), max_length=32, required=False)
    prenom = forms.CharField(widget=forms.TextInput(attrs={
        "placeholder": "Prénom", "class": "form-control"}), max_length=32, required=False)
    fonction = forms.CharField(widget=forms.TextInput(
        attrs={"placeholder": "Fonction", "class": "form-control"}), max_length=32, required=False)
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        "placeholder": "Email", "class": "form-control"}), max_length=80, required=False)
    telephone = forms.CharField(widget=forms.TextInput(
        attrs={"placeholder": "Téléphone", "class": "form-control"}), max_length=14, required=False)
    skype = forms.CharField(widget=forms.TextInput(attrs={
        "placeholder": "Skype", "class": "form-control"}), max_length=32, required=False)
    categories = SimpleArrayField(forms.CharField(widget=forms.TextInput(), required=False))
    siret = forms.CharField(widget=forms.TextInput(attrs={
        "placeholder": "Siret", "class": "form-control", "onkeyup": "this.value = this.value.toUpperCase();"}),
        min_length=14, max_length=14)
    nom_partenaire = forms.CharField(widget=forms.TextInput(
        attrs={"placeholder": "Dénomination", "class": "form-control"}), max_length=32, required=False)


class CustomerForm(forms.Form):
    bases = forms.MultipleChoiceField(choices=BASE_CHOICES, required=False)
    nom = forms.CharField(widget=forms.TextInput(
        attrs={"placeholder": "Nom", "class": "form-control"}), max_length=32, required=False)
    prenom = forms.CharField(widget=forms.TextInput(attrs={
        "placeholder": "Prénom", "class": "form-control"}), max_length=32, required=False)
    fonction = forms.CharField(widget=forms.TextInput(
        attrs={"placeholder": "Fonction", "class": "form-control"}), max_length=80, required=False)
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        "placeholder": "Email", "class": "form-control"}), max_length=80, required=False)
    telephone_fixe = forms.CharField(widget=forms.TextInput(
        attrs={"placeholder": "Téléphone fixe", "class": "form-control"}), max_length=14, required=False)
    telephone_mobile = forms.CharField(widget=forms.TextInput(
        attrs={"placeholder": "Téléphone mobile", "class": "form-control"}), max_length=14, required=False)
    leviers = SimpleArrayField(forms.CharField(), required=False)
    thematiques = SimpleArrayField(forms.CharField(), required=False)
    thematiques_blacklist = SimpleArrayField(forms.CharField(), required=False)
    siret = forms.CharField(widget=forms.TextInput(attrs={
        "placeholder": "Siret", "class": "form-control", "onkeyup": "this.value = this.value.toUpperCase();"}),
        min_length=14, max_length=14)
    nom_entreprise = forms.CharField(widget=forms.TextInput(
        attrs={"placeholder": "Dénomination", "class": "form-control"}), max_length=32, required=False)
    commentaire = forms.CharField(widget=forms.Textarea(
        attrs={"placeholder": "Commentaires", "class": "form-control"}), max_length=2048, required=False)
    code_postal = forms.CharField(widget=forms.TextInput(
        attrs={"placeholder": "Code postal", "class": "form-control"}), max_length=5, required=False)
    skype = forms.CharField(widget=forms.TextInput(attrs={
        "placeholder": "Skype", "class": "form-control"}), max_length=32, required=False)

class UserForm(forms.Form):
    admin = forms.BooleanField(required=False)
    civilite = forms.CharField()
    nom = forms.CharField(widget=forms.TextInput(
        attrs={"placeholder": "Nom","class": "form-control"}), max_length=32)
    prenom = forms.CharField(widget=forms.TextInput(attrs={
        "placeholder": "Prénom", "class": "form-control"}), max_length=32, required=False)
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        "placeholder": "Email","class": "form-control"}), max_length=80)
    mot_de_passe = forms.CharField(widget=forms.TextInput(
        attrs={"placeholder": "Mot de passe","class": "form-control"}), max_length=32, required=False)
    description = forms.CharField(widget=forms.Textarea(
        attrs={"placeholder": "Description","class": "form-control"}), max_length=2048, required=False)

class ThemeForm(forms.Form):
    libelle = forms.CharField(widget=forms.TextInput(
        attrs={"class": "form-control"}), max_length=32)


class BlacklistThemeForm(forms.Form):
    libelle = forms.CharField(widget=forms.TextInput(
        attrs={"class": "form-control"}), max_length=32)


class LevierForm(forms.Form):
    libelle = forms.CharField(widget=forms.TextInput(
        attrs={"class": "form-control"}), max_length=32)


class ModeleEconomiqueForm(forms.Form):
    libelle = forms.CharField(widget=forms.TextInput(
        attrs={"class": "form-control"}), max_length=32)


class CategorieForm(forms.Form):
    libelle = forms.CharField(widget=forms.TextInput(
        attrs={"class": "form-control"}), max_length=32)


class CampaignForm(forms.Form):
    libelle = forms.CharField(widget=forms.TextInput(
        attrs={"placeholder": "Libellé","class": "form-control"}), max_length=32)
    id_tradedoubler = forms.IntegerField(widget=forms.NumberInput(
        attrs={"placeholder": "Identifiant tradedoubler", "class": "form-control"}), required=False)
    client = forms.CharField(max_length=32)
    partenaires = SimpleArrayField(forms.CharField(), required=False)
    traffic_manager = forms.CharField(max_length=32)
    reporter = forms.CharField(max_length=32)
    commercial = forms.CharField(max_length=32)
    statut = forms.CharField(max_length=32)
    date_debut = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Date de début", "class": "form-control"}), required=False)
    date_fin = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Date de fin", "class": "form-control"}), required=False)
    levier = forms.CharField(widget=forms.TextInput(
        attrs={"placeholder": "Levier", "class": "form-control"}), max_length=32, required=False)
    modele_eco = forms.CharField(widget=forms.TextInput(
        attrs={"placeholder": "Modèle économique", "class": "form-control"}), max_length=32, required=False)
    tarif = forms.FloatField(widget=forms.NumberInput(
        attrs={"placeholder": "Tarif", "class": "form-control"}))
    prix_vendu = forms.FloatField(widget=forms.NumberInput(
        attrs={"placeholder": "Prix de vente", "class": "form-control"}), required=False)
    prix_achat = forms.FloatField(widget=forms.NumberInput(
        attrs={"placeholder": "Prix d'achat", "class": "form-control"}), required=False)
    objectif_mensuel = forms.FloatField(widget=forms.NumberInput(
        attrs={"placeholder": "Objectif mensuel", "class": "form-control"}), required=False)
    objectif_ca_mois = forms.FloatField(widget=forms.NumberInput(
        attrs={"placeholder": "Objectif CA mois en cours", "class": "form-control"}), required=False)
    trend = forms.FloatField(widget=forms.NumberInput(
        attrs={"placeholder": "Trend", "class": "form-control"}), required=False)
    trend_fin_mois = forms.FloatField(widget=forms.NumberInput(
        attrs={"placeholder": "Trend fin de mois", "class": "form-control"}), required=False)
    jour_reporting = forms.CharField(max_length=32)
    ca_realise = forms.BooleanField(required=False)
    achat_realise = forms.BooleanField(required=False)
    marge_realise = forms.BooleanField(required=False)
    nb_leads = forms.IntegerField(widget=forms.NumberInput(
        attrs={"placeholder": "Nombre de leads", "class": "form-control"}), required=False)
    nb_cliques = forms.IntegerField(widget=forms.NumberInput(
        attrs={"placeholder": "Nombre de cliques", "class": "form-control"}), required=False)
    nb_cliques_uniques = forms.IntegerField(widget=forms.NumberInput(
        attrs={"placeholder": "Nombre de cliques uniques", "class": "form-control"}), required=False)
    nb_ventes = forms.IntegerField(widget=forms.NumberInput(
        attrs={"placeholder": "Nombre de ventes", "class": "form-control"}), required=False)
    nb_affiliates = forms.IntegerField(widget=forms.NumberInput(
        attrs={"placeholder": "Nombre d'affiliations", "class": "form-control"}), required=False)
