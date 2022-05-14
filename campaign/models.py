from django.db import models
from django.utils.text import slugify

import shortuuid

from campaign.managers import ScenarioManager


class BaseModel(models.Model):
    user = models.ForeignKey('account.User', on_delete=models.CASCADE)
    organization = models.ForeignKey('account.Organization', on_delete=models.CASCADE, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Domain(BaseModel):
    name = models.CharField(max_length=255, unique=True)
    public_key = models.TextField(blank=True)

    class Meta:
        db_table = "domain"

    def __str__(self):
        return self.name


class SendingProfile(BaseModel):
    sender = models.CharField(max_length=255, help_text="Friendly sender name",)
    prefix = models.CharField(max_length=255, help_text="Prefix of sender (partition before @)", )
    domain = models.ForeignKey('Domain', on_delete=models.CASCADE)
    is_verified_smtp_dns = models.BooleanField(default=False, help_text="Is domain verified for SMTP server")
    is_verified_landing_page_dns = models.BooleanField(default=False, help_text="Is domain verified for Landing Page DNS")

    class Meta:
        db_table = "sending_profile"

    def __str__(self):
        return f"{self.sender} <{self.prefix}@{self.domain}>"

    @property
    def full_sender_address(self):
        return f"{self.sender} <{self.prefix}@{self.domain}>"


class BaseEmailTemplate(BaseModel):
    name = models.CharField(max_length=255)
    subject = models.CharField(max_length=255)
    content = models.TextField()

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class EmailTemplate(BaseEmailTemplate):

    class Meta:
        db_table = "email_template"


class RecipientGroup(BaseModel):
    name = models.CharField(max_length=255)

    class Meta:
        db_table = "recipient_group"

    def __str__(self):
        return self.name


class Recipient(BaseModel):
    rid = models.CharField('Recipient ID', max_length=10, unique=True, help_text="Unique ID for tracking")
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True, max_length=255)
    company = models.CharField(max_length=255, blank=True)
    department = models.CharField(max_length=255, blank=True)
    position = models.CharField(max_length=255, blank=True)


    class Meta:
        db_table = "recipient"

    def __str__(self):
        return f"{self.name}-{self.email}"

    def save(self, *args, **kwargs):
        if not self.rid:
            rid = shortuuid.ShortUUID().random(length=7)
            self.rid = rid
        super().save(*args, **kwargs)

    def filter_by_department(self, department):
        return self.objects.filter(department=department)


class BaseLandingPage(BaseModel):
    REDIRECT_CHOICES = [
        ('custom-url', 'Custom URL',),
        ('phished-url', 'Phished URL',),
    ]
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, help_text='Unique slug for landing page')
    content = models.TextField()
    redirect_url = models.CharField(max_length=255, blank=True)
    redirect_url_type = models.CharField(
        max_length=70, choices=REDIRECT_CHOICES, blank=True
    )

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class LandingPage(BaseLandingPage):
    TYPE_CHOICES = [
        ('site-based', 'Site Based',),
        ('attachment-based', 'Attachment Based',),
    ]
    based_type = models.CharField(choices=TYPE_CHOICES, max_length=50, blank=True)

    class Meta:
        db_table = "landing_page"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not self.slug:
            if LandingPage.objects.filter(user=self.user, slug=slugify(self.name)).exists():
                self.slug = slugify(self.name) + '-' + str(self.id)
            else:
                self.slug = slugify(self.name)
            self.save()


class Tag(BaseModel):
    name = models.CharField(max_length=255)

    class Meta:
        db_table = "tag"

    def __str__(self):
        return self.name


class Scenario(BaseModel):
    name = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)
    email_template = models.ForeignKey(EmailTemplate, on_delete=models.SET_NULL, null=True)
    landing_page = models.ForeignKey(LandingPage, on_delete=models.SET_NULL, null=True)
    tags = models.ManyToManyField('Tag', related_name="tags", blank=True)
    is_global = models.BooleanField(default=False, help_text="Is scenario globally available for users")

    objects = ScenarioManager()

    class Meta:
        db_table = "scenario"

    def __str__(self):
        return self.name

    @property
    def get_tags(self):
        return self.tags.filter(user=self.user)

    @property
    def is_ready(self):
        """Check if DNS records are verified
        """
        if self.email_template and self.landing_page:
            if all([
                self.email_template.domain.is_verified_smtp_dns,
                self.landing_page.domain.is_verified_landing_page_dns
            ]):
                return True
