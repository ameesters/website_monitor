website_monitor
===============

A simple gtk ui for monitoring websites, released on the BSD 2-clause licence, see LICENCE for more information.

### Be warned, this is a work in progress, things will be broken!

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
* Add website.
* Edit website.
* Delete website.
* Open website in browser.
* Proper validation on adding a website.
* Set timeout from GUI.
* Setting update interval from GUI.
* Mute website option.
* Refactor the code using DRY/DIE principle.
* Tracking history
  * uptime
  * ping
  * number of requests per visit
  * date last modified
  * Size of the webpage
  * External links
* Export options
  * HTML
  * PDF
  
