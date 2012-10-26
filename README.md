website_monitor
===============

A simple gtk ui for monitoring websites

Be warned, this is a work in progress, things will be broken!

# Setup:
<b>Make sure the pygtk module is installed, and a gtk libs of version 2.0 or higher.</b>

First we need to clone this repository, so open a comandline and enter:
```bash
git clone git@github.com:ameesters/website_monitor.git
cd website_monitor/
sqlite3 site_monitor.db
chmod +x init_db.py
```
then proceed to edit init_bd.py in your favorite editor, there is a list called SITES in there where you can add your sites, then save the file and exit.

finally run the command and the application should start:
```bash
./init_db.py
chmod +x quick-check-gtk.py
./quick-check-gtk.py
```
if not, please use the issue tracker!