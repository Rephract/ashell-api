import re
from campaign.models import Domain
from campaign.utils.constants import DNSConfigs

SMTP_HOST = config('SMTP_HOST')

from dns.resolver import Resolver

class DNSConfig():
    def __init__(self, domain):
        self.smtp_host: str = settings.SMTP_HOST
        self.domain: Domain = domain

    def get_resolver(self):
        dns_nameservers = [
            item.address for server in DNSConfigs.RESOLVE_NAMESERVERS 
            for item in Resolver().resolve(server)
        ]
        resolver = Resolver()
        resolver.nameservers = dns_nameservers
        return resolver

    def get_result(self, domain: Domain):
        resolver = self.get_resolver()

        mx_record = resolver.resolve(domain.name, "MX")[0].to_text()
        txt_record_spf = resolver.resolve(domain.name, "TXT")[0].to_text()
        txt_record_pkey = "".join(
            resolver.resolve(f"mta1._domainkey.{domain.name}", "TXT")[0].to_text().replace('"', '').split()
        )

        return {"mx": mx_record, "txt_spf": txt_record_spf, "txt_pkey": txt_record_pkey}
    
    def validate_result(self):
        result = self.get_result(self.domain)
        match_spf = re.match(f'^"{DNSConfigs.TXT_SPF_RECORD}"$', result['txt_spf'])

        if SMTP_HOST not in result['mx']:
            return f"MX record is not correct. Current value: {result['mx'], SMTP_HOST}"

        if not result["txt_pkey"] == self.domain.public_key:
            return f"TXT record for public key is not correct. Current value ends with: ...{result['txt_pkey'][-80:]}"

        if not match_spf:
            return f"TXT record for spf is not correct. Current value: {result['txt_spf']}"

        self.domain.is_verified_dns = True
        self.domain.save()
        # tasks.set_opendkim_for_domain.delay(domain.name)
        return "DNS records successfully verified."
