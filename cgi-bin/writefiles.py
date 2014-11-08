#!/usr/bin/env python3

# Copia files nel .bak

import shutil

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

shutil.copyfile("config.json", "config.json.bak")
shutil.copyfile("weektsp.json", "weektsp.json.bak")
shutil.copyfile("temperature.csv", "temperature.csv.bak")

print("Copia terminata")

# End body/End html
print("""
</body>
</html>
""")
