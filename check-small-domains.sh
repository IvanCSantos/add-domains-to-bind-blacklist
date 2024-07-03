#!/bin/zsh

# This script is here in order to find small domains, which may be incorrected inserted in the list. For example,
# somethings the list comes with a domain like "arandomdomain.c om.br". The space between that domain may cause the
# format-domain-list.py to create entries for two domains: "arandomdomain.c" and "om.br". This is not desired, and 
# I am working on improving the format-domain-list.py to be as acurate as possible.
# So this script is useful only to help debugging the problematic cases format-domain-list.py doesn't catch automatically

problematicSize=7;

count=1; 
for i in $(cat domainsToBLock.txt); do 
    size=$(echo ${i} | awk '{print length}');
    if [[ ${size} -lt ${problematicSize} ]]; then 
        echo "Line [${count}] ${i}"; 
    fi; 
    count=$(expr ${count} + 1); 
done