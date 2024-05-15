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

# Creates backup copy of previous 3 versions of /etc/bind/blacklist/blacklisted.zones
def backupOriginalFile(src):
  if(os.path.isfile('/etc/bind/blacklist/blacklisted.zones.bak3')):
    os.remove('/etc/bind/blacklist/blacklisted.zones.bak3')
  
  if(os.path.isfile('/etc/bind/blacklist/blacklisted.zones.bak2')):
    shutil.move('/etc/bind/blacklist/blacklisted.zones.bak2', '/etc/bind/blacklist/blacklisted.zones.bak3')
  
  if(os.path.isfile('/etc/bind/blacklist/blacklisted.zones.bak1')):
    shutil.move('/etc/bind/blacklist/blacklisted.zones.bak1', '/etc/bind/blacklist/blacklisted.zones.bak2')

  shutil.copyfile(src, '/etc/bind/blacklist/blacklisted.zones.bak1')

def writeToBindBlacklist(domainListToBlock):
  if(len(domainListToBlock) > 0):
    backupOriginalFile(bindBlackListFilePath)
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