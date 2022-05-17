from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status

from campaign.models import Domain, LandingPage, SendingProfile, Scenario
from campaign.tests.base import BaseTestCase
from campaign.tests.factories import DomainFactory, EmailTemplateFactory, LandingPageFactory, SendingProfileFactory

User = get_user_model()


class ScenarioViewSetTest(BaseTestCase):

    def test_scenario_list(self):
        list_url = reverse('campaigns:scenario-list')
        queryset = Scenario.objects.filter(organization=self.user.profile.organization)

        response = self.client.get(list_url)
        self.assertEqual(response.data.get('count'), len(queryset))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_scenario_create(self):
        domain = DomainFactory()
        sending_profile = SendingProfileFactory(
            domain_id=domain.id,
            is_verified_dns=True
        )
        landing_page = LandingPageFactory()
        email_template = EmailTemplateFactory()

        create_url = reverse('campaigns:scenario-list')
        data = {
            'name': 'Test Scenario',
            'description': "Test desc",
            'email_template': email_template.id,
            'landing_page': landing_page.id,
            'sending_profile': sending_profile.id,
            'is_draft': False
        }

        res = self.client.post(create_url, data=data, format="json")
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        scenario = Scenario.objects.filter(organization=self.user.profile.organization).first()
        self.assertEqual(scenario.name, data['name'])

    def test_scenario_create_unverified_dns(self):
        domain = DomainFactory()
        sending_profile = SendingProfileFactory(
            domain_id=domain.id,
            is_verified_dns=False
        )
        landing_page = LandingPageFactory()
        email_template = EmailTemplateFactory()

        create_url = reverse('campaigns:scenario-list')
        data = {
            'name': 'Test Scenario',
            'description': "Test desc",
            'email_template': email_template.id,
            'landing_page': landing_page.id,
            'sending_profile': sending_profile.id,
            'is_draft': False
        }

        res = self.client.post(create_url, data=data, format="json")
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
