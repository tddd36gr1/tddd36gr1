#!/usr/bin/env python2.5
# coding=utf8

import gtk
import hildon
import pango
import pygtk
import sys
import kartkomponent.gui
import kartkomponent.gps
import kartkomponent.map_xml_reader
import kartkomponent.data_storage



 
class HelloWorldApp(hildon.Program, gtk.Window):
  def __init__(self):
    hildon.Program.__init__(self)
    
    self.window = hildon.Window()
    self.window.connect("destroy", gtk.main_quit)
    self.window.connect("key-press-event", kartkomponent.gui.app.on_key_press)
    self.add_window(self.window)
    self.window.fullscreen()
    self.window.set_title('a title')
    
    
    ##    creates a color
    color = gtk.gdk.color_parse('#FFFFFF')
    color2 = gtk.gdk.color_parse('#FFFFFF')
    
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
    self.main_hbox.set_size_request(690, 450)
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
    self.event_hbox.set_size_request(690, 450)
    self.event_hbox.pack_start(self.eventTable, True, True, 0)
    self.eventlayout = gtk.Layout(None, None)
    self.eventlayout.set_size(700, 400)
    self.eventTable.attach(self.eventlayout, 0, 1, 0, 1, gtk.FILL|gtk.EXPAND, gtk.FILL|gtk.EXPAND, 0, 0)
    self.eventlayout.modify_bg(gtk.STATE_NORMAL, color2)
    self.eventlabel = gtk.Label("Uppdrag: Rädda en katt")
    self.eventlayout.put(self.eventlabel, 10, 0)
    self.check_button = gtk.CheckButton(label="kryssa för avklarat", use_underline=True)
    self.eventlayout.put(self.check_button, 10, 30)
    self.check_button.connect("clicked", self.Send_to_DB)
    
    ##    creates map hbox
    self.mapTable = gtk.Table(1, 1, False)
    self.map_hbox = gtk.HBox(homogeneous=False, spacing=0)
    self.map_hbox.set_size_request(690, 450)
    self.map_hbox.pack_start(self.mapTable, True, True, 0)
    self.maplayout = gtk.Layout(None, None)
    self.maplayout.set_size(700, 400)
    self.mapTable.attach(self.maplayout, 0, 1, 0, 1, gtk.FILL|gtk.EXPAND, gtk.FILL|gtk.EXPAND, 0, 0)
    self.maplayout.modify_bg(gtk.STATE_NORMAL, color2)

    ##    loads the map data and puts on the hbox
    self.mapView = kartkomponent.gui.app.view
    self.mapView.set_size_request(650, 400)
    self.maplayout.put(self.mapView, 10, 0)
    
    ## 

    ##    imports a picture
    imageEvent = gtk.Image()
    imageEvent.set_from_file("menybilder/uppdrag2.jpg")
    
    imageCompass = gtk.Image()
    imageCompass.set_from_file("menybilder/kompass2.jpg")
    
    imageTelephone = gtk.Image()
    imageTelephone.set_from_file("menybilder/telefon2.jpg")
    
    imageMsg = gtk.Image()
    imageMsg.set_from_file("menybilder/brev2.jpg")
    
    imageOff = gtk.Image()
    imageOff.set_from_file("menybilder/off.jpg")
    

    
    ##    vertical buttons
    self.button1 = gtk.Button()
    self.button1.add(imageEvent)
    self.button1.connect("clicked", self.EventView)
    self.button1.set_size_request(80,70)
    self.layout.put(self.button1, 0, 100)
    
    self.button2 = gtk.Button()
    self.button2.add(imageCompass)
    self.button2.connect("clicked", self.MapView)
    self.button2.set_size_request(80,70)
    self.layout.put(self.button2, 0, 0)
    
    
    self.button3 = gtk.Button()
    self.button3.add(imageTelephone)
    self.button3.connect("clicked", gtk.main_quit)
    self.button3.set_size_request(80,70)
    self.layout.put(self.button3, 0, 200)
    
    self.button4 = gtk.Button()
    self.button4.add(imageMsg)
    self.button4.connect("clicked", self.MainView)
    self.button4.set_size_request(80,70)
    self.layout.put(self.button4, 0, 300)
    
    self.button5 = gtk.Button()
    self.button5.add(imageOff)
    self.button5.connect("clicked", gtk.main_quit)
    self.button5.set_size_request(80,70)
    self.layout.put(self.button5, 0, 400)
    
    ##    horisontal buttons for the map hbox
    self.button6 = gtk.Button()
    self.button6.connect("clicked", self.Show_gps_pos)
    self.button6.set_size_request(150,30)
    self.button6.set_label("Visa pos.")
    self.maplayout.put(self.button6, 100, 400)
    
    self.button7 = gtk.Button()
    self.button7.connect("clicked", gtk.main_quit)
    self.button7.set_size_request(150,30)
    self.maplayout.put(self.button7, 300, 400)
    
    self.button8 = gtk.Button()
    self.button8.connect("clicked", gtk.main_quit)
    self.button8.set_size_request(150,30)
    self.maplayout.put(self.button8, 500, 400)
    
    ##    top label  
    label = gtk.Label("Nokia n810")
    label.set_size_request(500,50)
    label.set_alignment(xalign=0.5, yalign=0)
    label.modify_font(pango.FontDescription("sans 12"))
    self.layout.put(label, 100, 0)
    
  def CreateBoxes(self):
    self.layout.put(self.event_hbox, 100, 25)
    self.layout.put(self.map_hbox, 100, 25)
    self.layout.put(self.main_hbox, 100, 25)
    
    
  def HideBoxes(self):
    self.main_hbox.hide()
    self.event_hbox.hide()
    self.map_hbox.hide()
    
    ##    Function that changes hbox
  def MainView(self,widget, data = None):
    self.HideBoxes()
    self.main_hbox.show_all()
    
    ##    Function that changes to event view
  def EventView(self,widget, data = None):
    self.HideBoxes()
    self.event_hbox.show_all()
    
    ##    Function that changes to map view
  def MapView(self,widget, data = None):
    self.HideBoxes()
    self.map_hbox.show_all()
    
  def Send_to_DB(self,widget, data = None):
    print "Laddar in avklarat i databasen"

  def run(self):
    self.CreateBoxes()
    self.window.show_all()
    gtk.main() 
    
  def Show_gps_pos(self,widget, data = None):
    latt = kartkomponent.gps.get_gps_lat
    
    lonn = kartkomponent.gps.get_gps_lon
    mapxml = kartkomponent.map_xml_reader.MapXML("kartkomponent/map.xml")
    self.map = kartkomponent.data_storage.MapData(mapxml.get_name(), mapxml.get_levels())
    self.map.add_object("Shape1", kartkomponent.data_storage.MapObject({"longitude":15.5879, "latitude":58.4000},"arc(x - 5, y - 5, 10, 0, 2 * math.pi)","set_source_rgb(0, 0, 0)"))
    self.HideBoxes()
    self.map_hbox.show_all()
 
app = HelloWorldApp()
app.run()