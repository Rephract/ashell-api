from django.contrib.auth import get_user_model
from django.conf import settings
from rest_framework.test import APITestCase
from django.urls import reverse

from account.models import Organization


User = get_user_model()

class BaseTestCase(APITestCase):

    def setUp(self) -> None:
        self.user = User.objects.create_user(
            username="testuser@mail.com",
            email="testuser@mail.com",
            password="testpass"
        )
        organization = Organization.objects.create(
            name="Test Organization",
            slug="test-organization"
        )
        self.user.profile.organization = organization
        self.user.profile.save(update_fields=['organization'])

        self.api_authorization()

    def api_authorization(self) -> None:
        from oauth2_provider.models import Application

        Application.objects.get_or_create(
            id=1,
            user=self.user,
            name = "Client Secrets",
            client_id=settings.AUTH_CLIENT_ID,
            client_secret=settings.AUTH_CLIENT_SECRET,
            client_type='public',
            authorization_grant_type="password"
        )

        response = self.client.post(
            reverse('oauth2_provider:token'),
            data={
                'grant_type': 'password',
                'username': self.user.email,
                'password': "testpass",
                'client_id': settings.AUTH_CLIENT_ID,
                'client_secret': settings.AUTH_CLIENT_SECRET,
            }
        )
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + response.json().get('access_token'))