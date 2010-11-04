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
    
    
    

    main_box_hbox = gtk.HBox()
    right_box_vbox.add(main_box_hbox)
 
    button = gtk.Button(("k1"))
    button.connect("clicked", gtk.main_quit)
    left_box_vbox.pack_start(button, expand=False, fill=False, padding=0)
    button.set_size_request(10,30)
    
    button2 = gtk.Button("k2")
    button2.connect("clicked", gtk.main_quit)
    left_box_vbox.pack_start(button2, expand=False, fill=False, padding=0)
    button2.set_size_request(10,30)
    
    button3 = gtk.Button("k3")
    button3.connect("clicked", gtk.main_quit)
    left_box_vbox.pack_start(button3, expand=False, fill=False, padding=0)
    button3.set_size_request(10,30)
    
    label = gtk.Label("Uber nokia super jattebra!     13:37 ")
    top_box_hbox.pack_start(label, False)
    label.set_size_request(500,50)
    
    self.window.fullscreen()
    self.window.set_title('hellu')
    
    
 
  def run(self):
    self.window.show_all()
    gtk.main()
 
app = HelloWorldApp()
app.run()