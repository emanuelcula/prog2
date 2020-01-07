import json

exersices_string = '''
{
	"uebungen": [
		{
			"Beschreibung": "Uebung 1",
			"Anzahl Teilnehmer": 6,
			"Material": "keines"
		 },
		 {
		 	"Beschreibung": "Uebung 1",
			"Anzahl Teilnehmer": 6,
			"Material": "keines"
			}
	]
}
'''

data = json.loads(exersices_string)
print(data)