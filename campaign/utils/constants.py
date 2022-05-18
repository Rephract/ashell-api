import os


class DNSConfigs:
    A_RECORD_LANDING_PAGE = os.environ.get("A_RECORD_LANDING_PAGE")
    TXT_SPF_RECORD = "v=spf1 mx ip4:test ~all"
    RESOLVE_NAMESERVERS = ['ns1.digitalocean.com',
                           'ns2.digitalocean.com', 'ns3.digitalocean.com']
    KEY_TABLE = "/etc/opendkim/KeyTable"
    SIGNING_TABLE = "/etc/opendkim/SigningTable"
    TRUSTED_HOSTS = "/etc/opendkim/TrustedHosts"
    OPENDKIM_USER_ID = "2"
    DOMAIN_BASH_SCRIPT_PATH = "./domain.sh"