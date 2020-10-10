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
    print(resp.json())
    resp.raise_for_status()

    return resp.json()

def filter_domain_records(recordsIn, searchkey, searchval):
    recordsout=[]
    for record in recordsIn:
        if record[searchkey] == searchval:
            recordsout.append(record)
    return recordsout

def filter_records_with_recordtype(recordsIn, typeValue):
    return filter_domain_records(recordsIn, 'rrset_type', typeValue)

def filter_records_with_recordvalue(recordsIn, typeValue):
    if type(typeValue) != []:
        typeValue = [typeValue]
    return filter_domain_records(recordsIn, 'rrset_values', typeValue)

def filter_records_with_recordname(recordsIn, nameValue):
    return filter_domain_records(recordsIn, 'rrset_name', nameValue)

def update_domain_record(domain, apiurl, apikey, matchtype, matchname, value, ttl=10800):
    endpoint = 'domains/%s/records/%s/%s' % (domain, matchname, matchtype)
    puturl = urljoin(apiurl, endpoint)

    body = {
        'rrset_ttl': ttl,
        'rrset_values': [value,],
    }
    resp = requests.put(puturl, json=body, headers={'X-Api-Key': apikey})
    resp.raise_for_status()

def get_ip_for_domain(domain, apiurl, apikey):
    """Get the current IP from the A record in the DNS zone """

    # # There may be more than one A record - we're interested in one with
    # # the specific name (typically @ but could be sub domain)
    domain_records = get_domain_records(domain, apiurl, apikey)
    domain_records = filter_records_with_recordtype(domain_records, 'A')
    domain_records = filter_records_with_recordname(domain_records, '@')
    if len(domain_records) > 0:
        return domain_records[0]['rrset_values'][0]
    else:
        return None

def get_ip_for_subdomain(domain, subdomain, apiurl, apikey):
    """Get the current IP from the A record in the DNS zone """

    # # There may be more than one A record - we're interested in one with
    # # the specific name (typically @ but could be sub domain)
    domain_records = get_domain_records(domain, apiurl, apikey)
    domain_records = filter_records_with_recordtype(domain_records, 'A')
    domain_records = filter_records_with_recordname(domain_records, subdomain)
    if len(domain_records) > 0:
        return domain_records[0]['rrset_values'][0]
    else:
        return None

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

def set_ip_for_domain(domain, apiurl, apikey, newip, ttl):
    """ Update Gandi record A=#newip """

    update_domain_record(domain=domain, apiurl=apiurl, apikey=apikey, matchtype='A', matchname='@', value=newip, ttl=ttl)

def set_ip_for_subdomain(domain, subdomain, apiurl, apikey, newip, ttl):
    """ Update Gandi record A=#newip """

    update_domain_record(domain=domain, apiurl=apiurl, apikey=apikey, matchtype='A', matchname=subdomain, value=newip, ttl=ttl)

def check_and_update_record_domain(domain, apiurl, apikey, ttl):
    current_ip = get_public_ip().strip()

    zone_ip = get_ip_for_domain(domain=domain, apiurl=apiurl, apikey=apikey).strip()

    if zone_ip == current_ip:
        print('Record up to date, returning ('+zone_ip+')')
    else:
        print('Updating record to ('+zone_ip+')')
        set_ip_for_domain(
            domain=domain, 
            apiurl=apiurl, 
            apikey=apikey, 
            newip=current_ip,
            ttl=ttl)
        print('DNS A record update complete - set to ', zone_ip)

def check_and_update_record_subdomain(domain, subdomain, apiurl, apikey, ttl):
    current_ip = get_public_ip().strip()

    zone_ip = get_ip_for_subdomain(domain=domain, subdomain=subdomain, apiurl=apiurl, apikey=apikey).strip()

    if zone_ip == current_ip:
        print('Record up to date, returning ('+zone_ip+')')
    else:
        print('Updating record to ('+zone_ip+')')
        set_ip_for_subdomain(
            domain=domain, 
            subdomain=subdomain,
            apiurl=apiurl, 
            apikey=apikey, 
            newip=current_ip,
            ttl=ttl)
        print('DNS A record update complete - set to ', zone_ip)

def main():
    apikey = get_env_variable('APIKEY', None)
    apiurl = get_env_variable('APIURL', 'https://dns.api.gandi.net/api/v5/')
    ttl = get_env_variable('TTL', 10800)
    domain = get_env_variable('DOMAIN', None)
    subdomain = get_env_variable('SUBDOMAIN', None)

    if apikey == None:
        print('Missing \'APIKEY\' from env. See https://docs.gandi.net/en/domain_names/advanced_users/api.html')
        sys.exit(1)

    if domain == None:
        print('Missing \'DOMAIN\' from env. Set this to the website we\'re updating')
        sys.exit(1)

    if subdomain != None:
        check_and_update_record_subdomain(
            domain=domain, 
            subdomain=subdomain, 
            apiurl=apiurl, 
            apikey=apikey, 
            ttl=ttl)
    else:
        check_and_update_record_domain(
            domain=domain, 
            apiurl=apiurl, 
            apikey=apikey, 
            ttl=ttl)



if __name__ == "__main__":
    main()
