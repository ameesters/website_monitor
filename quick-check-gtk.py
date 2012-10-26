#!/usr/bin/env python
import os, time, datetime, httplib, subprocess, sqlite3

import pygtk
pygtk.require('2.0')
import gtk

class SiteApp:
	
	def __init__(self):
		''' setup database'''
		conn = sqlite3.connect('site_monitor.db')
		self.c = conn.cursor()
		#self.get_sites = c.execute('SELECT url FROM sites')
		'''Create new window:'''
		self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
		self.window.set_title('Site Monitor')
		self.window.set_icon_from_file('website-icon.png')
		self.window.set_size_request(800,600)
		self.window.set_border_width(10)
		self.window.set_position(gtk.WIN_POS_CENTER_ALWAYS)
		self.window.connect("destroy", self.destroy)
		
		vbox = gtk.VBox(False, 8)

		button = gtk.Button("Refresh", stock=gtk.STOCK_REFRESH)
		button.set_size_request(20,20)
		button.connect("clicked", self.on_update_clicked)
		vbox.pack_start(button, False, False, 0)		
		
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
		treeView.set_rules_hint(True)
		
		sw.add(treeView)
		self.create_columns(treeView)
		self.window.add(vbox)
		self.window.show_all()
		
		
		
	def create_model(self):
		'''create the model - a ListStore'''
		self.store = gtk.ListStore(str, str, str, str)
		for site in self.c.execute('SELECT url FROM sites'):
			conn = httplib.HTTPConnection(site[0], timeout=10)
			conn.request("HEAD", "/")
			response = conn.getresponse()
			self.store.append([site[0], response.status, response.reason, datetime.datetime.now()])
			conn.close()
			
		return self.store


	def on_update_clicked(self, widget):
		'''update the model'''
		self.store.clear()
		self.status_bar.push(self.context_id, "Status: Starting update...")
		#self.store = gtk.ListStore(str, str, str, str)
		for site in self.c.execute('SELECT url FROM sites'):
			conn = httplib.HTTPConnection(site[0], timeout=10)
			conn.request("HEAD", "/")
			response = conn.getresponse()
			self.store.append([site[0], response.status, response.reason, datetime.datetime.now()])
			conn.close()
			
		self.status_bar.push(self.context_id, "Status: Update done")
		return self.store
		
	def timer_update(self):
		'''update the model'''
		self.store.clear()
		self.status_bar.push(self.context_id, "Status: Starting update...")
		#self.store = gtk.ListStore(str, str, str, str)
		
		for site in self.c.execute('SELECT url FROM sites'):
			conn = httplib.HTTPConnection(site[0], timeout=10)
			conn.request("HEAD", "/")
			response = conn.getresponse()
			self.store.append([site[0], response.status, response.reason, datetime.datetime.now()])
			conn.close()
			
		self.status_bar.push(self.context_id, "Status: Update done")
		return self.store
		
	def timer_check_status(self):
		for status in self.store:
			if int(status[1]) > 399:
				print status[1]				
				subprocess.call(['/usr/bin/canberra-gtk-play','--file','siren.ogg'])

		
	def create_columns(self, treeView):
		''' create the columns '''
		rendererText = gtk.CellRendererText()
		column = gtk.TreeViewColumn("Site", rendererText, text=0)
		column.set_sort_column_id(0)
		treeView.append_column(column)
 
		rendererText = gtk.CellRendererText()
		column = gtk.TreeViewColumn("Status", rendererText, text=1)
		column.set_sort_column_id(1)    
		treeView.append_column(column)
 
		rendererText = gtk.CellRendererText()
		column = gtk.TreeViewColumn("Reason", rendererText, text=2)
		column.set_sort_column_id(2)    
		treeView.append_column(column)
		
		rendererText = gtk.CellRendererText()
		column = gtk.TreeViewColumn("Last updated", rendererText, text=3)
		column.set_sort_column_id(3)    
		treeView.append_column(column)
 
 
	def destroy(self, widget, data=None):
		'''close the window and quit'''
		gtk.main_quit()
		return False

 
	def main(self):
		gtk.timeout_add(60*1000, self.timer_update)
		gtk.timeout_add(60*1000, self.timer_check_status)
		gtk.main()

if __name__ == "__main__":
	checksite = SiteApp()
	checksite.main()
		
		
		
		