# Gandi-DDNS
Dynamic DNS tool to update your hostname record to your computers public ip address

[![License](https://img.shields.io/badge/license-MIT-green.svg?style=flat)](https://github.com/ryandev/BlueSkies/blob/master/LICENSE) [![Docker](https://img.shields.io/docker/automated/ryandev/gandi-ldns)](https://hub.docker.com/repository/docker/ryandev/gandi-ldns)

## Usage (main record) 
For records `NAME='@'` `TYPE='A'`
```
docker run --rm -e "APIKEY=myapikey" -e "DOMAIN=mydomainname" ryandev/gandi-ldns
```
where `mydomainname` is the website you have registered on gandi.net you want updated to your public ip & `myapikey` is the *production* api key (see here for more info setting it up: https://docs.gandi.net/en/domain_names/advanced_users/api.html)
*Thats it!*
after running `mydomainname` will be pointing to your public ip address

## Usage (subdomain)
For records `NAME='$SUBDOMAIN'` `TYPE='A'` 
Same as above, except specify argument `SUBDOMAIN` example:
```
docker run --rm -e "APIKEY=myapikey" -e SUBDOMAIN="vpn" -e "DOMAIN=ryandev.com" ryandev/gandi-ldns
```
This runs the same as above, except, vpn.ryandev.com will be pointing to your public address now

### About
This project is forked from 
[auxym/gandi-ldns](https://github.com/auxym/gandi-ldns) &
[matt1/gandi-ddns](https://github.com/matt1/gandi-ddns)

