#!/usr/bin/env python3

# trova e modifica eseguendo il rispettivo "write*.py"

# Serve per controllare i files
import os

# Serve per il formato dati, il file di configurazione e`
# in struttura "json"
import json

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
print("""
<h2>Backup dei files</h2>
<p><b>Salva solo i files di configurazione e per scrupolo anche le temperature</b></p>
<br/>
<br/>
""")

print("<p><hr/></p><br/>")	# Stampa un linea orizzontale

# Start FORM input
# write*.py
print("<form action=\"/cgi-bin/writefiles.py\" method=\"post\">")
print("""
Non ci sono impostazioni, verranno creati o sovrascritti i files:
<ul>
<li>config.json.bak</li>
<li>weektsp.json.bak</li>
<li>temperature.csv.bak</li>
</ul>

""")

print("<center><input type=\"submit\" value=\"Backup\"></center>")
print("</form>")	# END form


# End body/End html
print("""
</body>
</html>
""")
