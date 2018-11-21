#! /usr/bin/python

import sys
import os

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
  addressToAdd = sys.argv[2:]
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
