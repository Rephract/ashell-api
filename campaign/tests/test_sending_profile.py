from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status

from campaign.models import Domain, SendingProfile
from campaign.tests.base import BaseTestCase

User = get_user_model()


class SendingProfileViewSetTest(BaseTestCase):

    def test_sending_profile_list(self):
        list_url = reverse('campaigns:sending-profile-list')
        queryset = SendingProfile.objects.filter(organization=self.user.profile.organization)

        response = self.client.get(list_url)
        self.assertEqual(response.data.get('count'), len(queryset))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_sending_profile_create(self):
        domain = Domain.objects.create(user=self.user, name="example.com")
        create_url = reverse('campaigns:sending-profile-list')
        data = {
            'sender': "Sender Name",
            'prefix': "sender.name",
            'domain': domain.id
        }

        res = self.client.post(create_url, data=data, format="json")
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        sending_profile = SendingProfile.objects.filter(organization=self.user.profile.organization).first()
        self.assertEqual(sending_profile.sender, data['sender'])

