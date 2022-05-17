from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status

from campaign.models import Domain, SendingProfile, Scenario
from campaign.tests.base import BaseTestCase

User = get_user_model()


class ScenarioViewSetTest(BaseTestCase):

    def test_scenario_list(self):
        list_url = reverse('campaigns:scenario-list')
        queryset = Scenario.objects.filter(organization=self.user.profile.organization)

        response = self.client.get(list_url)
        self.assertEqual(response.data.get('count'), len(queryset))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
