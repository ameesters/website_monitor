#!/usr/bin/env python
import os, time, datetime, httplib, socket, subprocess, sqlite3

import pygtk
pygtk.require('2.0')
import gtk

class SiteApp:
	
	def __init__(self):
		
		# setup database:
		self.conn = sqlite3.connect('site_monitor.db')
		self.c = self.conn.cursor()
		
		# Create new window:
		self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
		self.window.set_title('Site Monitor')
		self.window.set_icon_from_file('images/website_monitor.svg')
		self.window.set_size_request(800,600)
		self.window.set_border_width(10)
		self.window.set_position(gtk.WIN_POS_CENTER_ALWAYS)
		self.window.connect("destroy", self.destroy)
		
		vbox = gtk.VBox(False, 8)
		hbox = gtk.HBox(False, 3)
		vbox.pack_start(hbox, False, False, 0)
		
		self.website_url=gtk.Entry()
		self.website_url.set_activates_default(True)		
		hbox.pack_start(self.website_url, True, True, 0)

		# Add button:
		add_button = gtk.Button("Add", stock=gtk.STOCK_NEW)
		add_button.set_size_request(70,30)
		add_button.connect("clicked", self.add_new_website)
		hbox.pack_start(add_button, True, True, 0)		

		# Update button:
		update_button = gtk.Button("Refresh", stock=gtk.STOCK_REFRESH)
		update_button.set_size_request(70,30)
		update_button.connect("clicked", self.on_update_clicked)
		hbox.pack_start(update_button, True, True, 0)		
		
		# Scrolled window:
		sw = gtk.ScrolledWindow()
		sw.set_shadow_type(gtk.SHADOW_ETCHED_IN)
		sw.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
		vbox.pack_start(sw, True, True, 0)
		
		self.status_bar = gtk.Statusbar()      
		vbox.pack_start(self.status_bar, False, False, 0)
		self.status_bar.show()
		self.context_id = self.status_bar.get_context_id("Status")		
		
		self.store = self.create_model()
		treeView = gtk.TreeView(self.store)
		treeView.connect("row-activated", self.on_activated)
		treeView.set_rules_hint(True)
		
		sw.add(treeView)
		self.create_columns(treeView)
		self.window.add(vbox)
		self.window.show_all()
		
	def add_new_website(self, widget):
		url = self.website_url.get_text()
		self.c.execute('INSERT INTO sites(url, desc) VALUES(?,?)', (url, "Inital import comment"))
		self.conn.commit()
		self.status_bar.push(self.context_id, "Status: new website added!")
		self.website_url.set_text('')
		
	def create_model(self):
		'''create the model - a ListStore'''
		self.store = gtk.ListStore(str, str, str, str, str)
		for site in self.c.execute('SELECT site_id, url FROM sites'):
			try:
				conn = httplib.HTTPConnection(site[1], timeout=10)
				conn.request("HEAD", "/")
				response = conn.getresponse()
			except(httplib.HTTPResponse, socket.error) as ex:
				self.store.append([site[0], site[1], "504", "Gateway Timeout", datetime.datetime.now()])
			else:
				self.store.append([site[0], site[1], response.status, response.reason, datetime.datetime.now()])
			conn.close()
			
		return self.store


	def on_update_clicked(self, widget):
		'''update the model'''
		self.store.clear()
		self.status_bar.push(self.context_id, "Status: Starting update...")

		for site in self.c.execute('SELECT site_id, url FROM sites'):
			try:
				conn = httplib.HTTPConnection(site[1], timeout=10)
				conn.request("HEAD", "/")
				response = conn.getresponse()
			except(httplib.HTTPResponse, socket.error) as ex:
				self.store.append([site[0], site[1], "504", "Gateway Timeout", datetime.datetime.now()])
			else:
				self.store.append([site[0], site[1], response.status, response.reason, datetime.datetime.now()])
				
			conn.close()
			
		self.status_bar.push(self.context_id, "Status: Manual Update done")
		return self.store
		
	def timer_update(self):
		'''update the model trough the timer'''
		self.store.clear()
		self.status_bar.push(self.context_id, "Status: Starting update...")
		
		for site in self.c.execute('SELECT site_id, url FROM sites'):
			try:
				conn = httplib.HTTPConnection(site[1], timeout=10)
				conn.request("HEAD", "/")
				response = conn.getresponse()
			except(httplib.HTTPResponse, socket.error) as ex:
				self.store.append([site[0], site[1], "504", "Gateway Timeout", datetime.datetime.now()])
			else:
				self.store.append([site[0], site[1], response.status, response.reason, datetime.datetime.now()])
			conn.close()
			
		self.status_bar.push(self.context_id, "Status: Auto-Update done")
		return self.store
		
	def timer_check_status(self):
		for status in self.store:
			if int(status[2]) > 399:
				print status[2]				
				subprocess.call(['/usr/bin/canberra-gtk-play','--file','siren.ogg'])
				
	def right_click_menu(self, widget, event, data):
		if(event.button != 3):
			return False
		m = gtk.Menu()
		i = gtk.MenuItem("Hello")
		i.show()
		m.append(i)
		m.popup(None, None, None, event.button, event.time, None)
		return False

		
	def create_columns(self, treeView):
		''' create the columns '''
		rendererText = gtk.CellRendererText()
		column = gtk.TreeViewColumn("#", rendererText, text=0)
		column.set_sort_column_id(0)
		treeView.append_column(column)
		
		''' create the columns '''
		rendererText = gtk.CellRendererText()
		column = gtk.TreeViewColumn("Site", rendererText, text=1)
		column.set_sort_column_id(0)
		treeView.append_column(column)

		rendererText = gtk.CellRendererText()
		column = gtk.TreeViewColumn("Status", rendererText, text=2)
		column.set_sort_column_id(1)    
		treeView.append_column(column)

		rendererText = gtk.CellRendererText()
		column = gtk.TreeViewColumn("Reason", rendererText, text=3)
		column.set_sort_column_id(2)    
		treeView.append_column(column)
		
		rendererText = gtk.CellRendererText()
		column = gtk.TreeViewColumn("Last updated", rendererText, text=4)
		column.set_sort_column_id(3)    
		treeView.append_column(column)
		
	def on_activated(self, widget, row, col):
		model = widget.get_model()
		text = model[row][0] + " selected."
		self.status_bar.push(self.context_id, text)


	def destroy(self, widget, data=None):
		'''close the window and quit'''
		gtk.main_quit()
		return False


	def main(self):
		gtk.timeout_add(10*1000, self.timer_update)
		gtk.timeout_add(60*1000, self.timer_check_status)
		gtk.main()

if __name__ == "__main__":
	checksite = SiteApp()
	checksite.main()
		
		
		
		