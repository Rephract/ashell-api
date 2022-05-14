from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status

from campaign.models import Domain, EmailTemplate
from campaign.tests.base import BaseTestCase

User = get_user_model()


class EmailTemplateViewSetTest(BaseTestCase):

    def test_email_template_list(self):
        list_url = reverse('campaigns:email-template-list')
        queryset = EmailTemplate.objects.filter(organization=self.user.profile.organization)

        response = self.client.get(list_url)
        self.assertEqual(response.data.get('count'), len(queryset))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_email_template_create(self):
        create_url = reverse('campaigns:email-template-list')
        data = {
            "name": "Test email template",
            "subject": "Test subject",
            "content": "Test content"
        }

        res = self.client.post(create_url, data=data, format="json")
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        email_template = EmailTemplate.objects.filter(organization=self.user.profile.organization).first()
        self.assertEqual(email_template.name, data['name'])
    

