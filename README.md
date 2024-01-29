# add-domains-to-bind-blacklist
This is a simple script I created to add domains to a blacklist on Bind in order to comply with determinations imposed on ISPs by ANATEL from Brasil

# How to use it
ANATEL is an internet regulatory agency in Brazil, and regularly requests ISPs to block certain internet domains. Use this script in your recursive servers in order to blacklist those domains.
You need to create a directory under Bind DNS Server named `blacklist`. This directory will hold two important files:
 - blacklisted.zones
 - blockeddomains.db

The `blacklisted.zones` will keep a list of zones in which are blocked. The format for this file is the same way you define a domain in Bind:
```zone "domainname.com" {type master; file "/etc/bind/blacklist/blockeddomains.db";}```

The blockeddomains.db will hold the domain data, which in this case defines the domains RR as 127.0.0.1 (the loopback address). The `blockeddomains.db` have the following content:
```;
; BIND data file for example.local
;
$TTL    3600
@       IN      SOA     ns1.italine.com.br. suporte.italine.com.br. (
                            2023062601         ; Serial
                                  7200         ; Refresh
                                   120         ; Retry
                               2419200         ; Expire
                                  3600)        ; Default TTL
;

@       IN      NS      ns1.italine.com.br.
@       IN      NS      ns2.italine.com.br.

                A       127.0.0.1
*       IN      A       127.0.0.1
                AAAA    ::1
*       IN      AAAA    ::1
```

Add more domains to the blacklist by writing a file to `/tmp/blacklistdomains` with a list of domains, one domain by line:
```
domain1.com
domain2.com
```

Then run this script which will read the `/tmp/blacklistdomains` and add the domains to the `blacklisted.zones` if they aren't blocked.
```python3 add-domains-to-bind-blacklist.py```