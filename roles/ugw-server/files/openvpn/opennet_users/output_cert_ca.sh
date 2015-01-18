#/bin/bash/
#
# ACHTUNG: verwaltet via ansible - siehe https://wiki.opennet-initiative.de/wiki/Opennet_ansible
#
# output CA CN
# mathias mahnke, 2013-06-09
#
for file in ${PWD}/certs/*
do
  if [ ! -d "${file}" ]
  then
    cn=$(openssl x509 -subject -noout -in $file | awk '{split($0,array,"CN=")} END{print array[2]}' | awk '{split($0,array,"/")} END{print array[1]}')
    issuer=$(openssl x509 -issuer -in $file -noout | awk '{split($0,array,"CN=")} END{print array[2]}' | awk '{split($0,array,"/")} END{print array[1]}')
    serial=$(openssl x509 -serial -noout -in $file | sed 's/serial\=//')
    valid=$(openssl x509 -dates -noout -in $file | grep notAfter | sed 's/notAfter\=//')
    echo $cn $issuer $serial $valid
  fi
done;
