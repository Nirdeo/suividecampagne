from django.urls import path
from suivi_de_campagne import view_partner, view_signin_signup_reset, views

urlpatterns = [
    path("", view_signin_signup_reset.login_view, name="login"),
    path("home/", views.home, name="home"),
    path('logout/', view_signin_signup_reset.logout_user, name='logout'),
    path("forgot-password/", view_signin_signup_reset.forgot_password,
         name="forgot-password"),
    path("reset-password/", view_signin_signup_reset.reset_password,
         name="reset-password"),
    # path("partners/test", view_partner.partner_list, name="partner-list"),
    path("partner-detail/", view_partner.partner_detail,
         name="partner-detail"),
    path("partners/", view_partner.view_partner,
         name="view-partner"),
    path("partners-send/", view_partner.create_partner,
         name="create-partner"),
]
