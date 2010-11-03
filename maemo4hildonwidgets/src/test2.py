#!/usr/bin/env python2.5
import gtk
import hildon
 
class HelloWorldApp(hildon.Program):
  def __init__(self):
    hildon.Program.__init__(self)
 
    self.window = hildon.Window()
    self.window.connect("destroy", gtk.main_quit)
    self.add_window(self.window)
    
    vbox = gtk.VBox()
    self.window.add(vbox)
 
    topbox = gtk.HBox()
    vbox.pack_start(topbox, False)
 
    button = gtk.Button("Do not TOUCH")
    button.connect("clicked", gtk.main_quit)
    topbox.pack_start(button, False)
 
    label = gtk.Label("Hello World!")
    topbox.pack_start(label, False)
 
  def run(self):
    self.window.show_all()
    gtk.main()
 
app = HelloWorldApp()
app.run()