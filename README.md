website_monitor
===============

A simple gtk ui for monitoring websites, released on the BSD 2-clause licence, see LICENCE for more information.

### Be warned, this is a work in progress, things will be broken!

#screenshots:
![Website Monitor 0.1](https://raw.github.com/ameesters/website_monitor/master/docs/screenshots/site_monitor_001.png "Website Monitor 0.1")

# Setup:
<b>Make sure the pygtk module is installed, and a gtk libs of version 2.0 or higher.</b>

First we need to execute some commands, so open a comandline and enter:
```bash
$ git clone git@github.com:ameesters/website_monitor.git
$ cd website_monitor/
$ chmod +x init_db.py main.py
$ sqlite3 site_monitor.db
$ ./init_db.py
$ ./main.py
```
if not, please use the issue tracker!
PS) For people who get stuck in the sqlite shell try `.exit` ;-)

# Todo:
Currently these issues are blocking a beta release(list will be updated frequently):
* ~~Add website.~~
  * Proper validation on adding a website.
* Edit website.
* Delete website.
* Open website in browser.
* Set timeout from GUI.
* Setting update interval from GUI.
* Mute website option.
* Refactor the code using DRY/DIE principle.
* Move to a more MVC like structure.
* Add a proper menu
* Tracking history like:
  * uptime
  * ping
  * number of requests per visit
  * date last modified
  * Size of the webpage
  * External links
* Export/Backup options:
  * HTML
  * PDF
  * CSV
  
