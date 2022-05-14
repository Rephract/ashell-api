from rest_framework.viewsets import ModelViewSet
from campaign.api.serializers import DomainSerializer, EmailTemplateSerializer, LandingPageSerializer, SendingProfileSerializer
from campaign.models import Domain, EmailTemplate, LandingPage, SendingProfile


class BaseModelViewSet(ModelViewSet):
    def get_queryset(self):
        queryset = super().get_queryset().select_related('organization')
        return queryset
    
    def perform_create(self, serializer):
        serializer.save(
            user=self.request.user, 
            organization=self.request.user.profile.organization
        )


class DomainViewset(BaseModelViewSet):
    queryset = Domain.objects.all()
    serializer_class = DomainSerializer


class EmailTemplateViewset(BaseModelViewSet):
    queryset = EmailTemplate.objects.all()
    serializer_class = EmailTemplateSerializer


class LandingPageViewset(BaseModelViewSet):
    queryset = LandingPage.objects.all()
    serializer_class = LandingPageSerializer


class SendingProfileViewset(BaseModelViewSet):
    queryset = SendingProfile.objects.all()
    serializer_class = SendingProfileSerializer
