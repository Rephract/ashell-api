from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response


from campaign.api.serializers import DomainSerializer, EmailTemplateSerializer, LandingPageSerializer, ScenarioSerializer, SendingProfileSerializer
from campaign.models import Domain, EmailTemplate, LandingPage, Scenario, SendingProfile
from celery import current_app as app


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

    @action(detail=True, url_path='verify-dns', methods=['GET'])
    def verify_dns(self, request):
        
        task = app.send_task(
            'launcher.tasks.launch_campaign',
            args=[campaign.id],
            kwargs={
                "is_restart": campaign.is_remigrate
            }
        )

        return Response({
            "entities": serializer.data
        })

class EmailTemplateViewset(BaseModelViewSet):
    queryset = EmailTemplate.objects.all()
    serializer_class = EmailTemplateSerializer


class LandingPageViewset(BaseModelViewSet):
    queryset = LandingPage.objects.all()
    serializer_class = LandingPageSerializer


class SendingProfileViewset(BaseModelViewSet):
    queryset = SendingProfile.objects.all()
    serializer_class = SendingProfileSerializer


class ScenarioViewset(BaseModelViewSet):
    queryset = Scenario.objects.all()
    serializer_class = ScenarioSerializer

