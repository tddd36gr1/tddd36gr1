import gtk
import hildon
import pygtk
import gui_view_uppdragtest
    
def minaUpp():
      
    color = gtk.gdk.color_parse('#FF0000')
    
    eventTable = gtk.Table(1, 1, False)
    event_hbox2 = gtk.HBox(homogeneous=False, spacing=0)
    event_hbox2.set_size_request(690, 450)
    event_hbox2.pack_start(self.eventTable, True, True, 0)
    eventlayout = gtk.Layout(None, None)
    eventlayout.set_size(600, 400)
    eventTable.attach(self.eventlayout, 0, 1, 0, 1, gtk.FILL|gtk.EXPAND, gtk.FILL|gtk.EXPAND, 0, 0)
    eventlayout.modify_bg(gtk.STATE_NORMAL, color)
#    event_hbox2.show_all()
    return self.event_hbox2
    
    
    
        

  
  