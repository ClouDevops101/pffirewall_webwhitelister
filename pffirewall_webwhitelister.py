#! /usr/bin/python

import sys
import os
import socket
import re

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
      r1 = re.findall(r"^[a-z][a-z0-9+\-.]*://([a-z0-9\-._~%!$&'()*+,;=]+@)?([a-z0-9\-._~%]+|\[[a-z0-9\-._~%!$&'()*+,;=:]+\])",comment)
      domain = r1[0][1]
      addressToAdd = (lookup_host(domain))
      print "[" + domain + "]"
      comment = domain
  elif len(sys.argv) > 2:
      addressToAdd = sys.argv[2:]
  else:
      sys.exit(0)
  print addressToAdd
  list_ip = []

  with open(fic) as f:
      contents = f.read()
      # TODO : Add regex to not match 84.4.4.44 against 4.4.4.4
      for ip  in addressToAdd:
          if ip not in contents:
              list_ip.append(ip)  ## app
          else:
              print ip + " Already registred"
  if list_ip:
      AddIP_toFile(comment, list_ip, fic)
      os.system('pfctl -e -f /etc/pf.conf')


if __name__ == '__main__':

  main()
