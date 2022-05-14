from rest_framework.routers import SimpleRouter

from campaign.api import viewsets

router = SimpleRouter()
router.register(r'domains', viewsets.DomainViewset, basename='domain')
router.register(r'email-templates', viewsets.EmailTemplateViewset, basename='email-template')
router.register(r'landing-pages', viewsets.LandingPageViewset, basename='landing-page')
router.register(r'sending-profiles', viewsets.SendingProfileViewset, basename='sending-profile')

urlpatterns = [] + router.get_urls() 