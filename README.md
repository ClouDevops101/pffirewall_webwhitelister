# Pffirewall Web whitelister
<a href="http://bitly.com/2grT54q"><img src="https://cdn.codementor.io/badges/i_am_a_codementor_dark.svg" alt="I am a codementor" style="max-width:100%"/></a><a href="http://bitly.com/2grT54q"><img src="http://www.shinken-monitoring.org/img/LogoFrameworkBlack.png" height="50"> 
 [![Donate](https://www.paypalobjects.com/en_US/i/btn/btn_donateCC_LG.gif)](https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=WX4EKLLLV49WG)


Description : The purpose of this project is to build an intelligent Firewalling and make web surifing safer by using PF Firewall  


Requierements
================
Probably a shinken installation would be benefit 
then install requirements :
```bash
pip install -r requirements.txt 
```
Having a runing pf firewall on OPEN BSD or Mac osx

Create a file named "/etc/pf-files/www-trusted-server" to persist rules in 

```bash
sudo mkdir /etc/pf-files/
sudo touch www-trusted-server
```

Add this lines to the pf firewall 

```bash
# Trusted Web server
table <www_trusted_server> persist file "/etc/pf-files/www-trusted-server"

pass out log  proto tcp from any to  <www_trusted_server>   port  {https,https } keep state
``

Documentation
=============


Add a rule to Pf firewall table with a single IP  : 
Start : 
```bash
sudo ./pffirewall_webwhitelister.py "linkedIn" 185.63.144.1
```
The output should be as follow : 
```bash
['185.63.144.1']
185.63.144.1  Added

```

Now Add a rule to Pf firewall table with a multiple  IP  :
```bash
sudo ./pffirewall_webwhitelister.py "linkedIn" 185.63.144.1  185.63.143.1 185.63.142.1
```
The output should be as follow : 
```bash
['185.63.144.1']
185.63.144.1  Already registred
185.63.143.1  Added
185.63.142.1  Added

```


