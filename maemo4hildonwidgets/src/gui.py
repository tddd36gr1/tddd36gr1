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
    color = gtk.gdk.color_parse('#234fdb')
    table = gtk.Table(2, 2, False)
    self.window.add(table)
    


    #skapar layout
    self.layout = gtk.Layout(None, None)
    self.layout.set_size(600, 600)
    #self.layout.modify_bg(gtk.STATE_NORMAL, color)
    table.attach(self.layout, 0, 1, 0, 1, gtk.FILL|gtk.EXPAND, gtk.FILL|gtk.EXPAND, 0, 0)
    
    self.main_hbox = gtk.HBox(homogeneous=False, spacing=0)
    self.layout.put(self.main_hbox, 100, 100)
    
    labeltest2 = gtk.Label("weeee")
    self.main_hbox_testbox = gtk.HBox(homogeneous=False, spacing=0)
    self.main_hbox_testbox.pack_start(labeltest2, False)
    
    testlabel = gtk.Label("hej")
    self.main_hbox.pack_start(testlabel, False)
    

    #scrollbar
    vScrollbar = gtk.VScrollbar(None)
    table.attach(vScrollbar, 1, 2, 0, 1, gtk.FILL|gtk.SHRINK, gtk.FILL|gtk.SHRINK, 0, 0)    
    
    vAdjust = self.layout.get_vadjustment()
    vScrollbar.set_adjustment(vAdjust)

    #lagga in bild
    image = gtk.Image()
    image.set_from_file("testbild.gif")
    
    
    #lagga till knappar pa vertikal
    self.button1 = gtk.Button()
    self.button1.add(image)
    self.button1.connect("clicked", self.CallableChanger,"hej")
    self.button1.set_size_request(70,70)
    self.layout.put(self.button1, 0, 0)
    
    self.button2 = gtk.Button()
    self.button2.connect("clicked", gtk.main_quit)
    self.button2.set_size_request(70,70)
    self.layout.put(self.button2, 0, 100)
    
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
    
    #knappar horisontellt
    self.button6 = gtk.Button()
    self.button6.add(image)
    self.button6.connect("clicked", self.CallableChanger,"hej")
    self.button6.set_size_request(150,30)
    self.layout.put(self.button6, 100, 440)
    
    self.button7 = gtk.Button()
    self.button7.connect("clicked", gtk.main_quit)
    self.button7.set_size_request(150,30)
    self.layout.put(self.button7, 300, 440)
    
    button8 = gtk.Button()
    button8.add(image)
    button8.connect("clicked", gtk.main_quit)
    button8.set_size_request(150,30)
    self.layout.put(button8, 500, 440)
    
    
    # Label   
    label = gtk.Label("Uber nokia super jattebra!     13:37 ")
    label.set_size_request(500,50)
    label.set_alignment(xalign=0.5, yalign=0)
    label.modify_font(pango.FontDescription("sans 12"))
    self.layout.put(label, 100, 0)
    
    #kod for fullscreen och label
    self.window.fullscreen()
    self.window.set_title('hellu') 
 
  def CallableChanger(self,widget, data = None):
    self.main_hbox.destroy()
    self.layout.put(self.main_hbox_testbox, 100, 100)
    self.window.show_all()
    
        
        #self.button2.set_label(data)
        
        
  def run(self):
    
    self.window.show_all()
    gtk.main()
    
  
        
 
app = HelloWorldApp()
app.run()