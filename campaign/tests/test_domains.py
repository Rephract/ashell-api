import json

from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status

from campaign.models import Domain
from campaign.tests.base import BaseTestCase

User = get_user_model()


class DomainViewSetTest(BaseTestCase):

    def test_domain_list(self):
        list_url = reverse('campaigns:domain-list')
        queryset = Domain.objects.filter(user=self.user)

        response = self.client.get(list_url)
        self.assertEqual(response.data.get('count'), len(queryset))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_domain_create(self):
        domain_create_url = reverse('campaigns:domain-list')
        data = {
            "name": "example.com",
        }
        res = self.client.post(domain_create_url, data=data, format="json")
        domains_qs = Domain.objects.filter(organization=self.user.profile.organization)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(domains_qs.first().name, data["name"])

    def test_domain_name_invalid(self):
        domain_create_url = reverse('campaigns:domain-list')
        data = {
            "name": "invalid",
        }

        res = self.client.post(domain_create_url, data=data, format="json")
        domains_qs = Domain.objects.filter(organization=self.user.profile.organization)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(len(domains_qs), 0)
    
    def test_duplicate_domain_invalid(self):
        domain_create_url = reverse('campaigns:domain-list')
        data = {
            "name": "example.com",
        }

        for _ in range(2):
            res = self.client.post(domain_create_url, data=data, format="json")
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        domain_count = Domain.objects.filter(name=data["name"]).count()
        self.assertEqual(domain_count, 1)
    
    def test_domain_name_update_restricted(self):
        domain_create_url = reverse('campaigns:domain-list')
        data = {
            "name": "example.com",
        }
        res = self.client.post(domain_create_url, data=data, format="json")

        domain = Domain.objects.filter(
            organization=self.user.profile.organization
        ).first()

        domain_update_url = reverse('campaigns:domain-detail', kwargs={"pk": domain.id})
        update_data = {
            "name": "updated.com"
        }
        res = self.client.patch(domain_update_url, data=update_data, format="json")
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(domain.name, data['name'])
  