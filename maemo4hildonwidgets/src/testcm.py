#!/usr/bin/env python2.5
import gtk
import hildon
 
class HelloWorldApp(hildon.Program):
  def __init__(self):
    hildon.Program.__init__(self)
      
    self.window = hildon.Window()
    self.window.connect("destroy", gtk.main_quit)
    self.add_window(self.window)
    
#    layout = gtk.Layout(hadjustment=500, vadjustment=500)
#    layout.set_size(750,750)
       
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
#    main_box_hbox.add(layout)
 
    button = gtk.Button("k1")
    button.connect("clicked", gtk.main_quit)
    left_box_vbox.pack_start(button, expand=True, fill=True, padding=5)
    button.set_size_request(70,70)
    
    button2 = gtk.Button("k2")
    button2.connect("clicked", gtk.main_quit)
    left_box_vbox.pack_start(button2, expand=True, fill=True, padding=5)
    button2.set_size_request(70,70)
    
    image = gtk.Image()
    image.set_from_file("testbild.gif")
    button3 = gtk.Button()
    button3.add(image)
    button3.connect("clicked", gtk.main_quit)
    left_box_vbox.pack_start(button3, expand=True, fill=True, padding=5)
    button3.set_size_request(70,70)
    
    button4 = gtk.Button("blubb")
    button4.connect("clicked", gtk.main_quit)
    left_box_vbox.pack_start(button4, expand=True, fill=True, padding=5)
    button4.set_size_request(70,70)
    
    button5 = gtk.Button("Ihhhh")
    button5.connect("clicked", gtk.main_quit)
    left_box_vbox.pack_start(button5, expand=True, fill=True, padding=5)
    button5.set_size_request(70,70)
    
    label = gtk.Label("Uber nokia super jattebra!     13:37 ")
    top_box_hbox.pack_start(label, False)
    label.set_size_request(650,50)
#    layout.put(label,0,0)
    
    self.window.fullscreen()
    self.window.set_title('hellu') 
 
  def run(self):
    self.window.show_all()
    gtk.main()
 
app = HelloWorldApp()
app.run()