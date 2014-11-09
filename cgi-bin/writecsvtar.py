#!/usr/bin/env python3

# Archivia

import shutil
import time

# Serve per la parte di gestione html in python
import cgi
import cgitb

import time
# Abilita gli errori al server web/http
cgitb.enable()


# Intestazione HTML
print("<!DOCTYPE html>")

print("""
<html>

<head>
  <title>ThermoRed</title>
  <meta name="GENERATOR" content="Midnight Commander (mcedit)">
  <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
  <meta name="Keywords" content="termoregolatore, thermo, temperatura, python">
  <meta name="Author" content="Davide">
</head>


<body>
""")	# End / Start body

## Inizio pagina web

print("L'archivio avra` un nome simile a questo:", "temperature.csv."+time.strftime("%y%m%d%H%M"),"<br/>")
print("Archiviazione ...<br/>")

shutil.copyfile("temperature.csv","temperature.csv."+time.strftime("%y%m%d%H%M"))

print("<br/>Archiviazione terminata<br/>")

# End body/End html
print("""
</body>
</html>
""")
