from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status

from campaign.models import LandingPage
from campaign.tests.base import BaseTestCase

User = get_user_model()


class LandingPageViewSetTest(BaseTestCase):

    def test_landing_page_list(self):
        list_url = reverse('campaigns:landing-page-list')
        queryset = LandingPage.objects.filter(organization=self.user.profile.organization)

        response = self.client.get(list_url)
        self.assertEqual(response.data.get('count'), len(queryset))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_landing_page_create(self):
        create_url = reverse('campaigns:landing-page-list')
        data = {
            "name": "Test landing page",
            "content": "Test content",
            "slug": "test-slug",
            "redirect_url_type": "custom-url",
            "redirect_url": "http://example.com"
        }

        res = self.client.post(create_url, data=data, format="json")
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        landing_page = LandingPage.objects.filter(organization=self.user.profile.organization).first()
        self.assertEqual(landing_page.name, data['name'])
    
    def test_landing_page_slug_unique(self):
        create_url = reverse('campaigns:landing-page-list')
        data = {
            "name": "Test landing page",
            "content": "Test content",
            "slug": "test-slug",
            "redirect_url_type": "custom-url",
            "redirect_url": "http://example.com"
        }
        for _ in range(2):
            res = self.client.post(create_url, data=data, format="json")
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        landing_page_count = LandingPage.objects.filter(slug=data['slug']).count()
        self.assertEqual(landing_page_count, 1)
