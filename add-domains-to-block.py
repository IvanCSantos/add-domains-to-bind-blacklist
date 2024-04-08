import re

# INPUTS
# The file with a list of domains to add to blacklist
domainListToBlockFilePath = '/tmp/blacklistdomains'
# The file in which all blocked domains are kept and read by Bind DNS Server
bindBlackListFilePath = '/etc/bind/blacklist/blacklisted.zones'

def getAlreadyBlockedDomains(bindBlackListFilePath):
  bindBlackList = list()
  file = open(bindBlackListFilePath, 'r')
  for line in file:
    regexSubstring = re.findall(r'"([^"]*)"', line.lower())
    if not regexSubstring:
      continue
    domain = regexSubstring[0]
    bindBlackList.append(domain)
  file.close()
  return bindBlackList


def readFromBlacklistFile(domainListFilePath, alreadyBlockedDomainList):
  domainListToBlock = list()
  file = open(domainListFilePath, 'r')
  for line in file:
    domain = line.lower().rstrip()
    if not domain:
      continue
    if(domain not in alreadyBlockedDomainList and domain not in domainListToBlock):
      domainListToBlock.append(domain)
  file.close()
  return domainListToBlock

def writeToBindBlacklist(domainListToBlock):
  file = open(bindBlackListFilePath, 'a')
  for domain in domainListToBlock:
    file.write('zone \"{0}\" {{type master; file \"/etc/bind/blacklist/blockeddomains.db\";}};\n'.format(domain))
  file.close()
  print("Added {} domains to blacklist".format(len(domainListToBlock)))

alreadyBlockedDomainList = getAlreadyBlockedDomains(bindBlackListFilePath)
domainListToBlock = readFromBlacklistFile(domainListToBlockFilePath, alreadyBlockedDomainList)
writeToBindBlacklist(domainListToBlock)