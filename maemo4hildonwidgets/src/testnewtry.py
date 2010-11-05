#!/usr/bin/env python2.5

import gtk
import hildon
import pango
import pygtk
import sys

class CallableChanger:
    def __call__(self, *args):
        testlabel2 = gtk.Label("hejsaaaan")
        main_hbox.pack_start(testlabel2, False)
        HelloWorldApp.run()
        
 
class HelloWorldApp(hildon.Program):
  def __init__(self):
    hildon.Program.__init__(self)
    
    self.window = hildon.Window()
    self.window.connect("destroy", gtk.main_quit)
    self.add_window(self.window)
    color = gtk.gdk.color_parse('#234fdb')
    color2 = gtk.gdk.color_parse('#335fdb')
    table = gtk.Table(2, 2, False)
    self.window.add(table)
    


    #skapar layout
    self.layout = gtk.Layout(None, None)
    self.layout.set_size(600, 600)
    self.layout.modify_bg(gtk.STATE_NORMAL, color)
    table.attach(self.layout, 0, 1, 0, 1, gtk.FILL|gtk.EXPAND, gtk.FILL|gtk.EXPAND, 0, 0)
    
    main_hbox = gtk.HBox(homogeneous=False, spacing=0)
    self.layout.put(main_hbox, 100, 100)
    
    testlabel = gtk.Label("hej")
    main_hbox.pack_start(testlabel, False)
    

    #scrollbar
    vScrollbar = gtk.VScrollbar(None)
    table.attach(vScrollbar, 1, 2, 0, 1, gtk.FILL|gtk.SHRINK, gtk.FILL|gtk.SHRINK, 0, 0)    
    
    vAdjust = self.layout.get_vadjustment()
    vScrollbar.set_adjustment(vAdjust)

    #lagga in bild
    image = gtk.Image()
    image.set_from_file("testbild.gif")
    
    #change window
    #def changeWindow(text):
    #    self.layout.modify_bg(gtk.STATE_NORMAL, color2)
    #    apa = gtk.Label(text)
    
    #lagga till knappar
    button1 = gtk.Button()
    button1.add(image)
    button1.connect("clicked", CallableChanger())
    button1.set_size_request(70,70)
    self.layout.put(button1, 0, 0)
    
    button2 = gtk.Button()
    button2.add(image)
    button2.connect("clicked", gtk.main_quit)
    button2.set_size_request(70,70)
    self.layout.put(button2, 0, 100)
    
    button3 = gtk.Button()
    button3.add(image)
    button3.connect("clicked", gtk.main_quit)
    button3.set_size_request(70,70)
    self.layout.put(button3, 0, 200)
    
    button4 = gtk.Button()
    button4.add(image)
    button4.connect("clicked", gtk.main_quit)
    button4.set_size_request(70,70)
    self.layout.put(button4, 0, 300)
    
    button5 = gtk.Button()
    button5.add(image)
    button5.connect("clicked", gtk.main_quit)
    button5.set_size_request(70,70)
    self.layout.put(button5, 0, 400)
    
    
    # Label   
    label = gtk.Label("Uber nokia super jattebra!     13:37 ")
    label.set_size_request(500,50)
    label.set_alignment(xalign=0.5, yalign=0)
    label.modify_font(pango.FontDescription("sans 12"))
    self.layout.put(label, 100, 0)
    
    #kod for fullscreen och label
    self.window.fullscreen()
    self.window.set_title('hellu') 
 
  def run(self):
    
    self.window.show_all()
    gtk.main()
    
  
        
 
app = HelloWorldApp()
app.run()