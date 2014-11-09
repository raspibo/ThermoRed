#!/usr/bin/env python3

# Archivia temperature.csv

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
<h2>Archivia "temperature.csv"</h2>
<p>Verra` creato un file con estensione "data" del file "temperature.csv"</p>
<br/>
<br/>
""")

print("<p><hr/></p><br/>")	# Stampa un linea orizzontale

# Start FORM input
# write*.py
print("<form action=\"/cgi-bin/writecsvtar.py\" method=\"post\">")
print("""
Non ci sono impostazioni.<br/>
NON verra` ricreato "temperature.csv"
""")

print("<center><input type=\"submit\" value=\"Archivia 'temperature.csv'\"></center>")
print("</form>")	# END form


# End body/End html
print("""
</body>
</html>
""")
