from celery import shared_task
from . import models
import os
import subprocess


# parse the target scope
def get_wildcard(program_id):
    t = []
    program = models.Programs.objects.get(id=program_id)
    assets = models.Assets.objects.filter(program=program)
    for asset in assets:
        if asset.scope_type == "wildcard":
            t += asset.target
    return t


@shared_task()
def subdomain_enumeration(program_id):
    WILDCARD_PATH = "wildcards.txt"
    OUTPUT_SUB = "subdomains.txt"
    scope_wild = get_wildcard(program_id=program_id)
    if len(scope_wild) <= 0:
        raise ValueError("program has no wildcard.")
    
    try:
        with open(WILDCARD_PATH, "w+") as f:
            f.writelines(f"{s}\n" for s in scope_wild)
        result = subprocess.run(
            ["subfinder", "-dL", WILDCARD_PATH, "-silent", "-o", OUTPUT_SUB],
            capture_output=True,
            text=True,
            timeout=300,
            check=True
        )
        

    except:
        pass
@shared_task()
def dns_scan():
    pass

@shared_task()
def service_discovery(): # Httpx
    pass

@shared_task()
def asset_scoring(): # AI based scoring
    pass

@shared_task
def crawling(): # crawling using Katana and grab js files
    pass

@shared_task()
def JS_scan(): # AI js files scanning
    pass