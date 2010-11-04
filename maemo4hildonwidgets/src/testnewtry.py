#!/usr/bin/env python2.5
import gtk
import hildon
 
class HelloWorldApp(hildon.Program):
  def __init__(self):
    hildon.Program.__init__(self)
    
    self.window = hildon.Window()
    self.window.connect("destroy", gtk.main_quit)
    self.add_window(self.window)
    table = gtk.Table(2, 2, False)
    self.window.add(table)

    self.layout = gtk.Layout(None, None)
    self.layout.set_size(600, 600)
    table.attach(self.layout, 0, 1, 0, 1, gtk.FILL|gtk.EXPAND, gtk.FILL|gtk.EXPAND, 0, 0)

    vScrollbar = gtk.VScrollbar(None)
    table.attach(vScrollbar, 1, 2, 0, 1, gtk.FILL|gtk.SHRINK, gtk.FILL|gtk.SHRINK, 0, 0)    
    
    vAdjust = self.layout.get_vadjustment()
    vScrollbar.set_adjustment(vAdjust)

    image = gtk.Image()
    image.set_from_file("testbild.gif")
    
    button1 = gtk.Button()
    button1.add(image)
    button1.connect("clicked", gtk.main_quit)
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

    
#    button = gtk.Button(("k1"))
#    button.connect("clicked", gtk.main_quit)
#    left_box_vbox.pack_start(button, expand=False, fill=False, padding=0)
#    button.set_size_request(10,30)
#    
#    button2 = gtk.Button("k2")
#    button2.connect("clicked", gtk.main_quit)
#    left_box_vbox.pack_start(button2, expand=False, fill=False, padding=0)
#    button2.set_size_request(10,30)
#    
#    button3 = gtk.Button("k3")
#    button3.connect("clicked", gtk.main_quit)
#    left_box_vbox.pack_start(button3, expand=False, fill=False, padding=0)
#    button3.set_size_request(10,30)
#    
    label = gtk.Label("Uber nokia super jattebra!     13:37 ")
    label.set_size_request(500,50)
    self.layout.put(label, 100, 0)
    
    self.window.fullscreen()
    self.window.set_title('hellu')
    
    
 
  def run(self):
    self.window.show_all()
    gtk.main()
 
app = HelloWorldApp()
app.run()