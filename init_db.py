#!/usr/bin/env python
import sqlite3
conn = sqlite3.connect('site_monitor.db')

c = conn.cursor()

c.execute('''
CREATE TABLE IF NOT EXISTS sites(
	site_id INTEGER PRIMARY KEY AUTOINCREMENT,
	url TEXT, 
	desc TEXT
)''')

c.execute('''
CREATE TABLE IF NOT EXISTS servers(
	server_id INTEGER PRIMARY KEY AUTOINCREMENT,
	ip TEXT, 
	hostname TEXT
)
''')

print "db's created"

SITES = [
	"www.example.com",
	"www.google.com",
	"www.meesters-id.nl",
	"carolsingers.nl"
]

for site in SITES:
	c.execute('INSERT INTO sites(url, desc) VALUES(?,?)', (site, "Inital import comment"))
	print site, " added!"
conn.commit()
