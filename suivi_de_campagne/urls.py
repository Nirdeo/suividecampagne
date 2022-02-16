from django.urls import path
from suivi_de_campagne import view_partner, view_profile, view_tool, view_customer, view_user, view_signin_signup_reset, view_campaign, views
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
     path("user-detail/<str:identifier>", view_user.user_detail, name="user-detail"),
     path("user-detail/", view_user.user_detail, name="user-detail"),
     path("create-user/", view_user.create_user, name="create-user"),
     path("edit-user/<str:identifier>", view_user.edit_user, name="edit-user"),
     path("delete-user/<str:identifier>", view_user.delete_user, name="delete-user"),
     path("users-list/", view_user.list_user, name="list-user"),

     path("tools/", view_tool.view_tool, name="view-tool"),
     path("create-theme/", view_tool.create_theme, name="create-theme"),
     path("create-blacklist-theme/", view_tool.create_blacklist_theme, name="create-blacklist-theme"),
     path("create-levier/", view_tool.create_levier, name="create-levier"),
     path("create-modele-economique/", view_tool.create_modele_economique, name="create-modele-economique"),
     path("delete-theme/<str:identifier>", view_tool.delete_theme, name="delete-theme"),
     path("delete-blacklist-theme/<str:identifier>", view_tool.delete_blacklist_theme, name="delete-blacklist-theme"),
     path("delete-levier/<str:identifier>", view_tool.delete_levier, name="delete-levier"),
     path("delete-modele-economique/<str:identifier>", view_tool.delete_modele_economique, name="delete-modele-economique"),
     path("tools-list/", view_tool.list_tool, name="list-tool"),

     path("campaign-detail/<str:identifier>", view_campaign.campaign_detail, name="campaign-detail"),
     path("campaign-detail/", view_campaign.campaign_detail, name="campaign-detail"),
     path("create-campaign/", view_campaign.create_campaign, name="create-campaign"),
     path("edit-campaign/<str:identifier>", view_campaign.edit_campaign, name="edit-campaign"),
     path("delete-campaign/<str:identifier>", view_campaign.delete_campaign, name="delete-campaign"),
     path("campaigns-list/", view_campaign.list_campaign, name="list-campaign"),

     path("profile/<str:identifier>",view_profile.profile_detail, name="profile-detail"),
     path("profile/", view_profile.profile_detail, name="profile-detail"),
     path("edit-profile/<str:identifier>", view_profile.edit_profile, name="edit-profile"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
