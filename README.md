website_monitor
===============

A simple gtk ui for monitoring websites

Be warned, this is a work in progress, things will be broken!

# Setup:
First clone this repository, open a commandline and enter the directory.
From there, execute:
```bash
sqlite3 site_monitor.db
chmod +x init_db.py
```
then proceed to edit init_bd.py, there is a list called SITES in there where you can add your sites, then save the file and exit.

run
```bash
./init_db.py
```

then:
```bash
chmod +x quick-check-gtk.py
```
and finnaly run:
```
./quick-check-gtk.py
```

That should get you setup.