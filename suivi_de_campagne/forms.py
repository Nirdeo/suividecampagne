from django import forms


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
    categories = forms.CharField(widget=forms.TextInput(
        attrs={"placeholder": "Catégories", "class": "form-control"}), max_length=32, required=False)
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
        attrs={"placeholder": "Fonction", "class": "form-control"}), max_length=32, required=False)
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        "placeholder": "Email", "class": "form-control"}), max_length=80, required=False)
    telephone_fixe = forms.CharField(widget=forms.TextInput(
        attrs={"placeholder": "Téléphone fixe", "class": "form-control"}), max_length=14, required=False)
    telephone_mobile = forms.CharField(widget=forms.TextInput(
        attrs={"placeholder": "Téléphone mobile", "class": "form-control"}), max_length=14, required=False)
    leviers = forms.CharField(widget=forms.TextInput(
        attrs={"placeholder": "Leviers", "class": "form-control"}), max_length=32, required=False)
    thematiques = forms.CharField(widget=forms.TextInput(
        attrs={"placeholder": "Thématiques", "class": "form-control"}), max_length=32, required=False)
    thematiques_blacklist = forms.CharField(widget=forms.TextInput(
        attrs={"placeholder": "Thématiques blacklistées", "class": "form-control"}), max_length=32, required=False)
    siret = forms.CharField(widget=forms.TextInput(attrs={
        "placeholder": "Siret", "class": "form-control", "onkeyup": "this.value = this.value.toUpperCase();"}),
        min_length=14, max_length=14)
    nom_entreprise = forms.CharField(widget=forms.TextInput(
        attrs={"placeholder": "Dénomination", "class": "form-control"}), max_length=32, required=False)
    commentaire = forms.CharField(widget=forms.Textarea(
        attrs={"placeholder": "Commentaires", "class": "form-control"}), max_length=2048, required=False)
    code_postal = forms.CharField(widget=forms.TextInput(
        attrs={"placeholder": "Code postal", "class": "form-control"}), max_length=5, required=False)

class ThemeForm(forms.Form):
    libelle_theme = forms.CharField(widget=forms.TextInput(
        attrs={"class": "form-control"}), max_length=32, required=False)


class BlacklistThemeForm(forms.Form):
    libelle_blacklist_theme = forms.CharField(widget=forms.TextInput(
        attrs={"class": "form-control"}), max_length=32, required=False)


class LevierForm(forms.Form):
    libelle_levier = forms.CharField(widget=forms.TextInput(
        attrs={"class": "form-control"}), max_length=32, required=False)


class ModeleEconomiqueForm(forms.Form):
    libelle_modele_economique = forms.CharField(widget=forms.TextInput(
        attrs={"class": "form-control"}), max_length=32, required=False)
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
