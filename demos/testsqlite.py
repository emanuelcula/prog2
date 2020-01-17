import sqlite3

#Datenbank erstellen
connection = sqlite3.connect('exercises.db')
cursor = connection.cursor()

#Tabelle in Datenbank erstellen
sql = '''CREATE TABLE IF NOT EXISTS Warmup 
				(PID INTEGER PRIMARY KEY AUTOINCREMENT,
				 BESCHREIBUNG VARCHAR(250),
				 TEILNEHMER INT,
				 MATERIAL VARCHAR(250))'''

cursor.execute(sql)

#Daten in Tabelle einfügen
sql = "INSERT INTO Warmup (BESCHREIBUNG, TEILNEHMER, MATERIAL) VALUES ('TESTBESCHREIBUNG ERSTE UEBUNG', 6, 'KEINS')"

cursor.execute(sql)
connection.commit()
sql = 'SELECT * FROM Warmup'
cursor.execute(sql)

rows = cursor.fetchall()

for row in rows:
	print(row)

connection.close()