from django.db import models
import re

SCOPE_TYPE=[
    ("Domain", "domain"),
    ("Wildcard", "wildcard"),
]

ASSET_TYPE=[
    ("IP", "ip"),
    ("Domain", "domain"),
    ("URL", "url"),
    ("Subdomain", "subdomain"),
    ("Other", "other"),
]

class Programs(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    platform = models.URLField(max_length=255)
    def __str__(self):
        return self.name

class Scope(models.Model):
    program = models.ForeignKey(Programs, on_delete=models.CASCADE, related_name='scopes')
    scope_type = models.CharField(max_length=255, choices=SCOPE_TYPE)
    target = models.CharField(max_length=255)

    created_at = models.DateTimeField(auto_now_add=True)    
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Scope {self.program.name}: {self.target} - {self.scope_type} "
    
    def save(self, *args, **kwargs):
        domain = self.target
        if not re.match(r"^([a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}$", domain):
            raise ValueError("Invalid domain format")
        super().save(*args, **kwargs)


class Assets(models.Model): # Where DNS Queried results are stored (IP behiended domains, subdomains, urls, etc)
    program = models.ForeignKey(Programs, on_delete=models.CASCADE, related_name='assets')
    scope = models.ForeignKey(Scope, on_delete=models.CASCADE, related_name='assets')
    asset_type = models.CharField(max_length=255, choices=ASSET_TYPE)
    asset_value = models.CharField(max_length=255)

    created_at = models.DateTimeField(auto_now_add=True)    
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Asset {self.program.name}: {self.asset_value} - {self.asset_type} "

class DNSRecord(models.Model):
    program = models.ForeignKey(Programs, on_delete=models.CASCADE, related_name='dns_scans')
    asset = models.ForeignKey(Assets, on_delete=models.CASCADE, related_name='dns_scans')
    ips = models.JSONField()
    is_wildcard = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"DNS Record {self.program.name}: {self.asset.asset_value} - {self.ips} "

class HttpxScan(models.Model):
    program = models.ForeignKey(Programs, on_delete=models.CASCADE, related_name='httpx_scans')
    asset = models.ForeignKey(Assets, on_delete=models.CASCADE, related_name='httpx_scans')
    raw_output = models.JSONField()
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Httpx Scan {self.program.name}: {self.asset.asset_value} - {self.raw_output} "

class LiveAssets(models.Model):
    program = models.ForeignKey(Programs, on_delete=models.CASCADE, related_name='live_assets')
    asset = models.ForeignKey(Assets, on_delete=models.CASCADE, related_name='live_assets')
    is_live = models.BooleanField(default=False)
    scan = models.ForeignKey(HttpxScan, on_delete=models.SET_NULL, null=True, blank=True) 
    
    status_code = models.IntegerField(null=True, blank=True)
    title = models.CharField(max_length=255, null=True, blank=True)
    url = models.URLField(max_length=255, null=True, blank=True)
    ip = models.GenericIPAddressField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Live Asset {self.program.name}: {self.asset.asset_value} - {self.is_live} "

class EndpointsByAI(models.Model):
    pass

class CredentialsByAI(models.Model):
    pass

class XSSDiscover(models.Model):
    pass
class SSRFDiscover(models.Model):
    pass
