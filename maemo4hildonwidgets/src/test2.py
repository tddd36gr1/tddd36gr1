#!/usr/bin/env python2.5
 
import gtk
import hildon
 
window = hildon.Window()
window.connect("destroy", gtk.main_quit)
label = gtk.Label("Deutchland uber alles!")
window.add(label)
 
label.show()
window.show()
 
gtk.main()