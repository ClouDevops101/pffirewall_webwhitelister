#! /usr/bin/python

import sys
import os
import socket
import re

#IP resolution
def lookup_ip(addr):
   try:
       return socket.gethostbyaddr(addr)[0]
       #return socket.gethostbyaddr(addr)
   except socket.herror:
       return None, None, None

def lookup_host(host):
   try:
       #return socket.gethostbyname(host)
       return socket.gethostbyname_ex(host)[2:][0]
       #socket.gethostbyname_ex("caf.fr")
       #('caf.fr', [], ['195.101.92.10', '77.158.24.239'])
   except socket.gaierror:
       return None


def AddIP_toFile(comment,list_ip,file):
    f = open(file, "a+")
    f.write("# %s\n" % comment)
    for ip in list_ip:
        f.write("%s\n" % ip)
        print ip + " Added"
    f.close()


def main():
  fic="/etc/pf-files/www-trusted-server"
  comment = sys.argv[1]

  #print len(sys.argv)

  addressToAdd=[]
  if len(sys.argv) == 2:
      # Handle
      # pffirewall_webwhitelister.py http://12factor.net/frfrfrfrfr
      try:
        r1 = re.findall(r"^[a-z][a-z0-9+\-.]*://([a-z0-9\-._~%!$&'()*+,;=]+@)?([a-z0-9\-._~%]+|\[[a-z0-9\-._~%!$&'()*+,;=:]+\])",comment)
        domain = r1[0][1]
        addressToAdd = (lookup_host(domain))
        comment = domain
        print "[" + domain + "]"
      except:
        # Handle
        # pffirewall_webwhitelister.py 12factor.net
        print "not a url"
        addressToAdd = (lookup_host(comment))

  elif len(sys.argv) > 2:
      # pffirewall_webwhitelister.py http://12factor.net 52.71.139.107 52.45.248.161
      addressToAdd = sys.argv[2:]
  else:
      sys.exit(0)
  print addressToAdd
  list_ip = []

  with open(fic) as f:
      contents = f.read()
      # TODO : Add regex to not match 84.4.4.44 against 4.4.4.4
      for ip  in addressToAdd:
          # Ip not registred and a valid ip
          if ip not in contents:
              try:
                  # Handle
                  # pffirewall_webwhitelister.py  https://www.oreilly.com/ 1080:0:0:0:8:800:200C:417A
                  socket.inet_aton(ip)
                  list_ip.append(ip)
                  continue ## app
              except socket.error:
                  print "[WARN] : Not ipv4 address"
              try:
                  # Handle :
                  # pffirewall_webwhitelister.py  https://www.oreilly.com/ 1.1.1.3
                  socket.inet_pton(socket.AF_INET6,ip)
                  list_ip.append(ip)
                  continue
              except socket.error:
                  print "[WARN] : Not ipv6 address"
          else:
              print ip + " Already registred"
  if list_ip:
      AddIP_toFile(comment, list_ip, fic)
      os.system('pfctl -e -f /etc/pf.conf')


if __name__ == '__main__':

  main()
