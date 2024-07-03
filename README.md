# add-domains-to-bind-blacklist

This is a simple script I created to add domains to a blacklist on Bind in order to comply with determinations imposed on ISPs by ANATEL from Brasil

# How to use it

ANATEL is an internet regulatory agency in Brazil, and regularly requests ISPs to block certain internet domains. Use this script in your recursive servers in order to blacklist those domains.
You need to create a directory under Bind DNS Server named `blacklist`. This directory will hold two important files:

- blacklisted.zones
- blockeddomains.db

The `blacklisted.zones` will keep a list of zones in which are blocked. The format for this file is the same way you define a domain in Bind:

```
zone "domainname.com" {type master; file "/etc/bind/blacklist/blockeddomains.db";}
```

The `blockeddomains.db` will hold the domain data, which in this case defines the domains RR as 127.0.0.1 (the loopback address). The `blockeddomains.db` have the following content:

```;
; BIND data file for example.local
;
$TTL    3600
@       IN      SOA     ns1.fqdn. support.fqdn. (
                            2023062601         ; Serial
                                  7200         ; Refresh
                                   120         ; Retry
                               2419200         ; Expire
                                  3600)        ; Default TTL
;

@       IN      NS      ns1.fqdn.
@       IN      NS      ns2.fqdn.

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

Then run this script which will read the `/tmp/blacklistdomains` and add the domains to the `blacklisted.zones` if they aren't already blocked.

```
# python3 add-domains-to-bind-blacklist.py
```

# Helper script to generate the domain list

Since you will often receive the list of domains in a table in a PDF file (omg!), use the `format-domain-list.py` helper script to help you generate the list of domains which is(`domainsToBlock.txt`).
To do this, simply copy the table with domain data from the PDF file to a text file (`domains.txt`). Don't worry about removing headers, pagination data, blank lines, putting each domain on new line, etc. as the script will only search for domains even if there are multiple on the same line. Just make sure you copied everything from the PDF table (you may want to copy it to an excel spreadsheet before copying to the `domains.txt` file in order to visualize better what you got).

## Then run the format-domain-list.py script and the output of this script is the domainsToBlock.txt file:

The script will read the input file `domains.txt` with a list of domains + garbage (page headers, pagination, many domains separated by space on same line, etc) and will output `domainsToBlock.txt` with the domain list cleaned, one domain per line. This last file you will use with the `add-domains-to-block.py`, so copy this data to the `/tmp/blacklistdomains` mentioned earlier.
To use the helper script, run the following command:

```
python3 format-domain-list.py
```
