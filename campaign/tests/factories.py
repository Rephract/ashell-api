import factory
import factory.django
import factory.fuzzy
from django.utils.text import slugify

from campaign.models import Domain, EmailTemplate, LandingPage, SendingProfile


class DomainFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Domain

    user_id = 1
    organization_id = 1
    name = factory.Faker('domain_name')
    public_key = ""


class SendingProfileFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = SendingProfile

    user_id = 1
    organization_id = 1
    sender = factory.Faker('name')
    domain_id = None
    is_verified_dns = factory.fuzzy.FuzzyChoice(choices=[True, True, True, False])

    @factory.lazy_attribute
    def prefix(self):
        return self.sender.lower().replace(" ", "")

class EmailTemplateFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = EmailTemplate

    user_id = 1
    organization_id = 1
    name = factory.Faker('name')
    subject = 'Test Subject'
    content = factory.Faker('paragraph')


class LandingPageFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = LandingPage

    user_id = 1
    organization_id = 1
    name = factory.Faker('name')
    content = factory.Faker('paragraph')
    redirect_url = factory.Faker('url')
    redirect_url_type = "custom-url"

    @factory.lazy_attribute
    def slug(self):
        return slugify(self.name)
