# Gandi-DDNS
Dynamic DNS tool to update your hostname record to your computers public ip address

[![License](https://img.shields.io/badge/license-MIT-green.svg?style=flat)](https://github.com/ryandev/BlueSkies/blob/master/LICENSE) [![Docker](https://img.shields.io/docker/automated/ryandev/gandi-ldns)](https://hub.docker.com/repository/docker/ryandev/gandi-ldns)

## Usage
```
docker run --rm -e "APIKEY=myapikey" -e "DOMAIN=mydomainname" ryandev/gandi-ldns
```
where `mydomainname` is the website you have registered on gandi.net you want updated to your public ip & `myapikey` is the *production* api key (see here for more info setting it up: https://docs.gandi.net/en/domain_names/advanced_users/api.html)

*Thats it! maybe you'll want to put the above in cron, but that's everything*

### About
This project is forked from 
[auxym/gandi-ldns](https://github.com/auxym/gandi-ldns) &
[matt1/gandi-ddns](https://github.com/matt1/gandi-ddns)

