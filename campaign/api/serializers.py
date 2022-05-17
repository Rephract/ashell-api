from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify

import validators

from campaign.models import Domain, EmailTemplate, LandingPage, Scenario, SendingProfile

class DomainSerializer(serializers.ModelSerializer):

    class Meta:
        model = Domain
        fields = [
            'id',
            'name',
            'public_key'
        ]

        extra_kwargs = {
            'public_key': {'read_only': True},
        }

    def validate_name(self, value):
        if not validators.domain(value):
            raise serializers.ValidationError(_("Invalid domain name"))
        return value

    def update(self, instance, validated_data):
        if self.instance.name != validated_data['name']:            
            raise serializers.ValidationError(_("Domain name can't be changed once created."))
        return super().update(instance, validated_data)


class EmailTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailTemplate
        fields = [
            'id',
            'name',
            'subject',
            'content'
        ]


class LandingPageSerializer(serializers.ModelSerializer):
    class Meta:
        model = LandingPage
        fields = [
            'id',
            'name',
            'slug',
            'content',
            'redirect_url_type',
            'redirect_url'
        ]

    def validate_slug(self, value):
        return slugify(value)

    def validate_redirect_url(self, value):
        if not validators.url(value):
            raise serializers.ValidationError(_("Not a valid URL."))
        return value


class SendingProfileSerializer(serializers.ModelSerializer):
    domain = DomainSerializer(read_only=True)
    class Meta:
        model = SendingProfile
        fields = [
            'id',
            'sender',
            'prefix',
            'domain',
            'full_sender_address',  
            'is_verified_dns',
        ]

    def validate(self, attrs):
        domain = Domain.objects.filter(
            id=self.initial_data['domain']
        ).first()
        if not domain:
            raise serializers.ValidationError(_("Domain is not exists in this organization"))
        email_address = f"{attrs['prefix']}@{domain.name}"
        if not validators.email(email_address):
            raise serializers.ValidationError(_("Sender email address is not valid"))
        attrs['domain'] = domain
        return attrs


class ScenarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Scenario
        fields = [
            'id',
            'name',
            'description',
            'email_template',
            'landing_page',
            'sending_profile',
            'tags',
            'is_global',
            'is_draft'
        ]

    def validate_sending_profile(self, value):
        if not value.is_verified_dns and not self.initial_data['is_draft']:
            raise serializers.ValidationError(_("DNS records must be verified."))
        return value