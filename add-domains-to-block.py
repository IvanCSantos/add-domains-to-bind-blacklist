import re

# INPUTS
# The file with a list of domains to add to blacklist
domainListToBlockFilePath = '/tmp/blacklisteddomains'
# The file in which all blocked domains are kept and read by Bind DNS Server
bindBlackListFilePath = '/etc/bind/blacklist/blacklisted.zones'

# LISTS
domainListToBlock = list()

def getAlreadyBlockedDomains(bindBlackListFilePath):
  bindBlackList = list()
  file = open(bindBlackListFilePath, 'r')
  for line in file:
    regexSubstring = re.findall(r'"([^"]*)"', line.lower())
    domain = regexSubstring[0]
    bindBlackList.append(domain)
  file.close()
  return bindBlackList


def readFromBlacklistFile(domainListFilePath):
  file = open(domainListFilePath, 'r')
  for line in file:
    domain = line.lower()
    domainListToBlock.append(domain)
  file.close()

getAlreadyBlockedDomains(bindBlackListFilePath)