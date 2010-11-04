#!/usr/bin/env python2.5
import gtk
import hildon
 
class HelloWorldApp(hildon.Program):
  def __init__(self):
    hildon.Program.__init__(self)
    
    
    
    self.window = hildon.Window()
    self.window.connect("destroy", gtk.main_quit)
    self.add_window(self.window)
    
       
    main_hbox = gtk.HBox(homogeneous=False, spacing=0)
    self.window.add(main_hbox)
    
    left_box_vbox = gtk.VBox()
    main_hbox.add(left_box_vbox)
    
    right_box_vbox = gtk.VBox()
    main_hbox.add(right_box_vbox)
    
    top_box_hbox = gtk.HBox()
    right_box_vbox.add(top_box_hbox)
    #top_box_hbox.setSize(height=5, width=5)
    
    

    main_box_hbox = gtk.HBox()
    right_box_vbox.add(main_box_hbox)
 
    button = gtk.Button(("Quit"))
    button.connect("clicked", gtk.main_quit)
    left_box_vbox.pack_start(button, expand=True, fill=True, padding=0)
    
    button = gtk.Button("knapp2")
    button.connect("clicked", gtk.main_quit)
    left_box_vbox.pack_start(button, expand=True, fill=True, padding=0)
    
    button = gtk.Button("knapp3")
    button.connect("clicked", gtk.main_quit)
    left_box_vbox.pack_start(button, expand=True, fill=True, padding=0)
    
    
    label = gtk.Label("Uber nokia super jattebra!     13:37 ")
    top_box_hbox.pack_start(label, False)
 
 
  def run(self):
    self.window.show_all()
    gtk.main()
 
app = HelloWorldApp()
app.run()