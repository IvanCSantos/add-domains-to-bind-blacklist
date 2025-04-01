import re
import shutil
import os

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

# Creates backup copy of previous X versions of /etc/bind/blacklist/blacklisted.zones
def backupOriginalFile(src, qty=10):
  if(os.path.isfile(src + ".bak" + str(qty))):
    os.remove(src + ".bak" + qty)
  for i in range(qty, 1, -1):
    if(os.path.isfile(src + ".bak" + str(i-1))):
      shutil.move(src + ".bak" + str(i-1), src + ".bak" + str(i))
  shutil.copyfile(src, src + ".bak1")

def writeToBindBlacklist(domainListToBlock):
  if(len(domainListToBlock) > 0):
    backupOriginalFile(bindBlackListFilePath, 50)
    file = open(bindBlackListFilePath, 'a')
    for domain in domainListToBlock:
      file.write('zone \"{0}\" {{type master; file \"/etc/bind/blacklist/blockeddomains.db\";}};\n'.format(domain))
    file.close()
    print("Added {} domains to blacklist".format(len(domainListToBlock)))
  else:
    print("All domains already blocked. Nothing to do here")


alreadyBlockedDomainList = getAlreadyBlockedDomains(bindBlackListFilePath)
domainListToBlock = readFromBlacklistFile(domainListToBlockFilePath, alreadyBlockedDomainList)
writeToBindBlacklist(domainListToBlock)