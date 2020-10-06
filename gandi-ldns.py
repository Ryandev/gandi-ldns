#!/usr/bin/env python3


from urllib.parse import urljoin
import sys
import os
import socket
import requests

def get_env_variable(name, defaultvalue=''):
    """Get variable set in environment otherwise fallback to #defaultvalue"""

    val = os.environ.get(name)
    if val == None:
        val = defaultvalue
    return val

def get_domain_records(domain, apiurl, apikey):
    """Get all records in the DNS zone """

    endpoint = 'domains/%s/records' % domain
    urlfetch = urljoin(apiurl, endpoint)

    ip = '0.0.0.0'

    resp = requests.get(urlfetch, headers={'X-Api-Key': apikey})
    resp.raise_for_status()

    return resp.json()

def update_domain_record(domain, apiurl, apikey, matchtype, matchname, value, ttl=10800):
    endpoint = 'domains/%s/records/%s/%s' % (domain, matchname, matchtype)
    puturl = urljoin(apiurl, endpoint)

    body = {
        'rrset_ttl': ttl,
        'rrset_values': [value,],
    }
    print(body)
    resp = requests.put(puturl, json=body, headers={'X-Api-Key': apikey})
    resp.raise_for_status()

def filter_domain_records(recordsIn, searchkey, searchval):
    recordsout=[]
    for record in recordsIn:
        if record[searchkey] == searchval:
            recordsout.append(record)
    return recordsout

def get_zone_ip(domain, apiurl, apikey):
    """Get the current IP from the A record in the DNS zone """

    # # There may be more than one A record - we're interested in one with
    # # the specific name (typically @ but could be sub domain)
    domain_records = get_domain_records(domain, apiurl, apikey)
    domain_records = filter_domain_records(domain_records, 'rrset_type', 'A')
    domain_records = filter_domain_records(domain_records, 'rrset_name', '@')
    if len(domain_records) > 0:
        return domain_records[0]['rrset_values'][0]
    else:
        return None

def set_zone_ip(domain, apiurl, apikey, newip, ttl):
    """ Update Gandi record A=#newip """

    update_domain_record(domain=domain, apiurl=apiurl, apikey=apikey, matchtype='A', matchname='@', value=newip, ttl=ttl)

def get_public_ip():
    """ Get external IP """

    try:
        # Could be any service that just gives us a simple raw
        # ASCII IP address (not HTML etc)
        resp = requests.get("https://api.ipify.org")
    except requests.exceptions.HTTPError:
        print('Unable to external IP address.')
        sys.exit(2)

    return resp.text


def main():
    current_ip = get_public_ip().strip()

    apikey = get_env_variable('APIKEY', None)
    apiurl = get_env_variable('APIURL', 'https://dns.api.gandi.net/api/v5/')
    ttl = get_env_variable('TTL', 10800)
    domain = get_env_variable('DOMAIN', None)

    if apikey == None:
        print('Missing \'APIKEY\' from env. See https://docs.gandi.net/en/domain_names/advanced_users/api.html')
        sys.exit(1)

    if domain == None:
        print('Missing \'DOMAIN\' from env. Set this to the website we\'re updating')
        sys.exit(1)

    zone_ip = get_zone_ip(domain=domain, apiurl=apiurl, apikey=apikey).strip()

    if zone_ip == current_ip:
        print('Record up to date, returning ('+zone_ip+')')
    else:
        print('Updating record to ('+zone_ip+')')
        set_zone_ip(
            domain=domain, 
            apiurl=apiurl, 
            apikey=apikey, 
            newip=current_ip,
            ttl=ttl)
        print('DNS A record update complete - set to ', zone_ip)


if __name__ == "__main__":
    main()
