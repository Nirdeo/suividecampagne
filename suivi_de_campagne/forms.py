from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "Username", "class": "form-control"}))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={"placeholder": "Password", "class": "form-control"}))


class formulaire_forgot_password(forms.Form):
    email = forms.CharField(max_length=80)


class formulaire_reset_password(forms.Form):
    email = forms.CharField(max_length=32)


BASES_CHOICES = [
    ('interne', 'Interne'),
    ('externe', 'Externe'),
]


class PartnerForm(forms.Form):
    base = forms.MultipleChoiceField(
        required=False, widget=forms.CheckboxSelectMultiple(attrs={
            "class": "form-control"}), choices=BASES_CHOICES, )
    nom_contact = forms.CharField(widget=forms.TextInput(
        attrs={"class": "form-control"}), max_length=32, required=False)
    prenom = forms.CharField(widget=forms.TextInput(attrs={
        "class": "form-control"}), max_length=32, required=False)
    fonction = forms.CharField(widget=forms.TextInput(
        attrs={"class": "form-control"}), max_length=32, required=False)
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        "class": "form-control"}), max_length=32, required=False)
    telephone = forms.CharField(widget=forms.TextInput(
        attrs={"class": "form-control"}), max_length=32, required=False)
    skype = forms.CharField(widget=forms.TextInput(attrs={
        "class": "form-control"}), max_length=32, required=False)
    categories = forms.CharField(widget=forms.TextInput(
        attrs={"class": "form-control"}), max_length=32, required=False)
    siret = forms.CharField(widget=forms.TextInput(attrs={
        "class": "form-control", "onkeyup": "this.value = this.value.toUpperCase();"}), min_length=14, max_length=14)
    nom_partenaire = forms.CharField(widget=forms.TextInput(
        attrs={"class": "form-control"}), max_length=32, required=False)
