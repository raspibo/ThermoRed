ThermoRed
=========

CronoTermostato "ThermoRed" (Perche` inizialmente avevo pensato a un'interfaccia "rossa")

Lo scopo e\` realizzare sul Raspberry Pi un qualcosa di leggero e semplice,
cioe\` un programma modificabile da chiunque sappia digitare su una tastiera,
e che sia il piu` possibile intuitivo per l'utilizzatore.

Allo stato delle cose e\` un progetto a se\` stante, ma l'idea e\` che diventi
una centralina facente parte di un'impianto domotico .. ecc.ecc. ..



== Istruzioni ==

Per il test dell'intefaccia web non serve il collegamento della sonda di temperatura,
c\'e\` gia\` un "temperature.csv" che contiene alcuni dati.

Eseguite il webserver col comando:

  python3 python3webserver.py

collegatevi all'host dove lo avete messo in esecuzione, porta 8080, sono
attive solo le voci di menu funzionanti, non potete sbagliare (comunque declino
ogni responsabilita`, lo fate a vostro rischio e pericolo ;) ).
