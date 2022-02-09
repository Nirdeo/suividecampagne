from django.urls import path
from suivi_de_campagne import view_partner, view_customer, view_sidepage, view_signin_signup_reset, views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
     path("", view_signin_signup_reset.login_view, name="login"),
     path("home/", views.home, name="home"),
     path("logout/", view_signin_signup_reset.logout_user, name="logout"),
     path("forgot-password/", view_signin_signup_reset.forgot_password, name="forgot-password"),
     path("reset-password/", view_signin_signup_reset.reset_password, name="reset-password"),
     path("partner-detail/<str:identifier>", view_partner.partner_detail, name="partner-detail"),
     path("partner-detail/", view_partner.partner_detail, name="partner-detail"),
     path("create-partner/", view_partner.create_partner, name="create-partner"),
     path("edit-partner/<str:identifier>", view_partner.edit_partner, name="edit-partner"),
     path("delete-partner/<str:identifier>", view_partner.delete_partner, name="delete-partner"),
     path("partners-list/", view_partner.list_partner, name="list-partner"),
     path("customer-detail/<str:identifier>", view_customer.customer_detail, name="customer-detail"),
     path("customer-detail/", view_customer.customer_detail, name="customer-detail"),
     path("create-customer/", view_customer.create_customer, name="create-customer"),
     path("edit-customer/<str:identifier>", view_customer.edit_customer, name="edit-customer"),
     path("delete-customer/<str:identifier>", view_customer.delete_customer, name="delete-customer"),
     path("customers-list/", view_customer.list_customer, name="list-customer"),

     path("sidepages/", view_sidepage.view_sidepage, name="view-sidepage"),
     path("create-theme/", view_sidepage.create_theme, name="create-theme"),
     path("create-blacklist-theme/", view_sidepage.create_blacklist_theme, name="create-blacklist-theme"),
     path("create-levier/", view_sidepage.create_levier, name="create-levier"),
     path("create-modele-economique/", view_sidepage.create_modele_economique, name="create-modele-economique"),
     path("delete-theme/<str:identifier>", view_sidepage.delete_theme, name="delete-theme"),
     path("delete-blacklist-theme/<str:identifier>", view_sidepage.delete_blacklist_theme, name="delete-blacklist-theme"),
     path("delete-levier/<str:identifier>", view_sidepage.delete_levier, name="delete-levier"),
     path("delete-modele-economique/<str:identifier>", view_sidepage.delete_modele_economique, name="delete-modele-economique"),
     path("sidepages-list/", view_sidepage.list_sidepage, name="list-sidepage"),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
