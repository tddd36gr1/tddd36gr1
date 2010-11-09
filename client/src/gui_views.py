#!/usr/bin/env python2.5

import gtk
import hildon
import pango
import pygtk
import sys
        
 
class HelloWorldApp(hildon.Program):
  def __init__(self):
    hildon.Program.__init__(self)
    
    self.window = hildon.Window()
    self.window.connect("destroy", gtk.main_quit)
    self.add_window(self.window)
    self.window.fullscreen()
    self.window.set_title('a title')
    
    ##    creates a color
    color = gtk.gdk.color_parse('#234fdb')
    color2 = gtk.gdk.color_parse('red')
    
    ##    creates the table 2x2 onto the window
    table = gtk.Table(2, 2, False)
    self.window.add(table)

    ##    creates layout and puts into the top left corner of the table
    self.layout = gtk.Layout(None, None)
    self.layout.set_size(600, 600)
    table.attach(self.layout, 0, 1, 0, 1, gtk.FILL|gtk.EXPAND, gtk.FILL|gtk.EXPAND, 0, 0)
    self.layout.modify_bg(gtk.STATE_NORMAL, color)
    #code for modifying background color
   
    ##    creates a horisontal box onto the layout
    ##    inital main view
    self.mainTable = gtk.Table(1, 1, False)
    self.main_hbox = gtk.HBox(homogeneous=False, spacing=0)
    self.main_hbox.set_size_request(700, 400)
    self.layout.put(self.main_hbox, 75, 25)
    self.main_hbox.pack_start(self.mainTable, True, True, 0)
    self.mainlayout = gtk.Layout(None, None)
    self.mainlayout.set_size(700, 400)
    self.mainTable.attach(self.mainlayout, 0, 1, 0, 1, gtk.FILL|gtk.EXPAND, gtk.FILL|gtk.EXPAND, 0, 0)
    self.mainlayout.modify_bg(gtk.STATE_NORMAL, color2)
    self.mainlabel = gtk.Label("Mainbox")
    self.mainlayout.put(self.mainlabel, 10, 0)

    ##creates event hbox
    self.eventTable = gtk.Table(1, 1, False)
    self.event_hbox = gtk.HBox(homogeneous=False, spacing=0)
    self.event_hbox.set_size_request(700, 400)
    self.event_hbox.pack_start(self.eventTable, True, True, 0)
    self.eventlayout = gtk.Layout(None, None)
    self.eventlayout.set_size(700, 400)
    self.eventTable.attach(self.eventlayout, 0, 1, 0, 1, gtk.FILL|gtk.EXPAND, gtk.FILL|gtk.EXPAND, 0, 0)
    self.eventlayout.modify_bg(gtk.STATE_NORMAL, color2)
    self.eventlabel = gtk.Label("Eventbox")
    self.eventlayout.put(self.eventlabel, 10, 0)
    self.check_button = gtk.CheckButton(label="test", use_underline=True)
    self.eventlayout.put(self.check_button, 10, 30)
    
    self.check_button.connect("clicked", self.Send_to_DB)

    ##    imports a picture
    image = gtk.Image()
    image.set_from_file("testbild.gif")
    
    ##    vertical buttons
    self.button1 = gtk.Button()
    self.button1.add(image)
    self.button1.connect("clicked", self.ChangeHbox)
    self.button1.set_size_request(70,70)
    self.layout.put(self.button1, 0, 0)
    
    self.button2 = gtk.Button()
    self.button2.connect("clicked", self.EventView)
    self.button2.set_size_request(70,70)
    self.button2.set_label("U")
    self.layout.put(self.button2, 0, 100)
    
    self.button3 = gtk.Button()
    self.button3.connect("clicked", gtk.main_quit)
    self.button3.set_size_request(70,70)
    self.layout.put(self.button3, 0, 200)
    
    self.button4 = gtk.Button()
    self.button4.connect("clicked", gtk.main_quit)
    self.button4.set_size_request(70,70)
    self.layout.put(self.button4, 0, 300)
    
    self.button5 = gtk.Button()
    self.button5.connect("clicked", gtk.main_quit)
    self.button5.set_size_request(70,70)
    self.layout.put(self.button5, 0, 400)
    
    ##    horisontal buttons
    self.button6 = gtk.Button()
    self.button6.connect("clicked", gtk.main_quit)
    self.button6.set_size_request(150,30)
    self.layout.put(self.button6, 100, 440)
    
    self.button7 = gtk.Button()
    self.button7.connect("clicked", gtk.main_quit)
    self.button7.set_size_request(150,30)
    self.layout.put(self.button7, 300, 440)
    
    self.button8 = gtk.Button()
    self.button8.connect("clicked", gtk.main_quit)
    self.button8.set_size_request(150,30)
    self.layout.put(self.button8, 500, 440)
    
    ##    top label  
    label = gtk.Label("Nokia n810")
    label.set_size_request(500,50)
    label.set_alignment(xalign=0.5, yalign=0)
    label.modify_font(pango.FontDescription("sans 12"))
    self.layout.put(label, 100, 0)
    
    
  def RemoveBoxes(self):
    self.main_hbox.hide()
    self.event_hbox.hide()
    
    ##    Function that changes hbox
  def ChangeHbox(self,widget, data = None):
    self.RemoveBoxes()
    self.layout.put(self.main_hbox, 75, 25)
    self.main_hbox.show_all()
    
    ##    Function that changes to event view
  def EventView(self,widget, data = None):
    self.RemoveBoxes()
    self.layout.put(self.event_hbox, 75, 25)
    self.event_hbox.show_all()
    
  def Send_to_DB(self,widget, data = None):
    print "hej"

  def run(self):
    self.window.show_all()
    gtk.main() 
 
app = HelloWorldApp()
app.run()