# This file is licenced under WTFPL (see LICENSE.txt)
# Erik Eloff, 2010
#
# -*- coding: utf-8 -*-
import time
import gtk
import tilenames
import os.path
import gobject
from db import DatabaseWorker
from class_.base_objects import Mission, Employee


TILE_PATH="mapwidget/cache"
MAX_ZOOM_LEVEL=15
MIN_ZOOM_LEVEL=10

class Tile(object):
    """
    A tile represents a 256x256 image and covers a square of the map.
    """
    z, x, y = (0, 0, 0)
    loaded = False
    def __init__(self, x, y, z):
        """
        Constructs a tile with the specified x, y and z.
        """
        self.x = x
        self.y = y
        self.z = z

    def load(self):
        """
        Loads the tile from disk to memory.
        """
        tile_path = TILE_PATH + '/%s/%s/%s.png' % (self.z,self.x, self.y)
        if not os.path.exists(tile_path):
            tile_path = "mapwidget/no_image.png"
        self.pixbuf = gtk.gdk.pixbuf_new_from_file(tile_path)

class MapWidget(gtk.DrawingArea):
    """
    A widget that displays a map and allow panning with mouse and zooming
    with F7/F8. Those are mapped to +/- on the N810 device.

    Map implementation is based on slippy map. See:
    * http://wiki.openstreetmap.org/wiki/Slippy_Map
    * http://wiki.openstreetmap.org/wiki/Slippy_map_tilenames
    """
    tiles = {}
    _focus = (0,0)
    _zoom_level = MIN_ZOOM_LEVEL

    def __init__(self, lat, long, db):
        """
        Creates a new MapWidget focused on (lat, long) coordinates.
        """
        self.db = db
        self.object_counter = 0
        self.i = 0
        self.draw_icons = True
        
        
        """
        Adding placemark pictures
        """
        self.mission_pic = gtk.gdk.pixbuf_new_from_file_at_size('ikoner/Mission.png', 25, 25)
        self.employee_pic = gtk.gdk.pixbuf_new_from_file_at_size('trololo.jpg', 25, 25)
        
        gtk.DrawingArea.__init__(self)
        self._focus = (float(lat), float(long))
        self.movement_from = {"x": 0, "y":0}
        self.allow_movement = False
        self.last_movement_timestamp = 0.0
        #self.set_size_request(640, 480)
        self.window_in_fullscreen = False
        
        
        """
        Gets a list of all objects from the database
        """
        self.all_missions = self.db.get_all(Mission)
        self.all_employees = self.db.get_all(Employee)
        
        
        self.set_flags(gtk.CAN_FOCUS)
        self.connect("expose_event", self.handle_expose_event)

        self.connect("button_press_event", self.handle_button_press_event)
        
        self.connect("button_release_event", self.handle_button_release_event)
        self.connect("motion_notify_event", self.handle_motion_notify_event)
        self.connect("key_press_event", self.handle_key_press_event)
        self.set_events(gtk.gdk.BUTTON_PRESS_MASK |
                        gtk.gdk.BUTTON_RELEASE_MASK |
                        gtk.gdk.EXPOSURE_MASK |
                        gtk.gdk.LEAVE_NOTIFY_MASK |
                        gtk.gdk.POINTER_MOTION_MASK |
                        gtk.gdk.POINTER_MOTION_HINT_MASK)

        #self.draw_icons()
    def get_focus(self):
        return self._focus


    def set_focus(self, value):
        self._focus = value
        self.emit("focus-changed", self.focus)
        self.queue_draw()

 
    def get_zoom_level(self):
        return self._zoom_level


    def set_zoom_level(self, value):
        if value < MIN_ZOOM_LEVEL:
            self._zoom_level = MIN_ZOOM_LEVEL
        elif value > MAX_ZOOM_LEVEL:
            self._zoom_level = MAX_ZOOM_LEVEL
        else:
            self._zoom_level = value

        self.queue_draw()
    focus = property(get_focus, set_focus)
    zoom_level = property(get_zoom_level, set_zoom_level)
           
    def handle_key_press_event(self, widget, event):
        """
        Handles key presses while mapwidget has focus
        """
        if event.keyval == gtk.keysyms.F6:
            if self.window_in_fullscreen:
                self.window.unfullscreen()
            else:
                self.window.fullscreen()
        # Zoom -
        elif event.keyval == gtk.keysyms.F8:
            self.zoom_level -= 1
        # Zoom +
        elif event.keyval == gtk.keysyms.F7:
            self.zoom_level += 1

    def handle_button_press_event(self, widget, event):
        """
        Handles dragging of the map
        """
        # Grab focus when clicked, must be done to get key presses
        self.grab_focus()
        self.draw_icons = False

        self.movement_from["x"] = event.x
        self.movement_from["y"] = event.y
        
        
        self.last_movement_timestamp = time.time()
        self.allow_movement = True

        (x, y, w, h) = self.get_allocation()
        deltax = event.x - w/2
        deltay = event.y - h/2
                
        
        for objects in self.get_objects_from_db():
            self.object_counter = self.object_counter+1
            (d,e) = self._coord_to_pixel(objects.long, objects.lat)
                        
            if d < event.x < (d + 25):
                if (e) <event.y < (e + 25):          
                    self.allow_movement = False                   
                    self.popup()
                else:
                    self.allow_movement = True
                    
        self.object_counter = 0

        coord = self._pixel_to_coord(deltax, deltay)
        self.emit("map-clicked", coord)
        return True

    def handle_button_release_event(self, widget, event):
        self.allow_movement = False
        self.draw_icons = True
        return True

    def handle_motion_notify_event(self, widget, event):
        if self.allow_movement:
            if event.is_hint:
                x, y, state = event.window.get_pointer()
            else:
                x = event.x
                y = event.y
                state = event.state
                #self.draw_icons()

            # Check time since last event to filter out unintentional movement
            if time.time() > self.last_movement_timestamp + 0.1:
                deltax = self.movement_from["x"] - x
                deltay = self.movement_from["y"] - y

                self.movement_from["x"] = x
                self.movement_from["y"] = y

                # Move focus
                self.focus = self._pixel_to_coord(deltax, deltay)

        return True

    def handle_expose_event(self, widget, event):
        self.draw()
        #self.draw_icons()
        return False

    def draw(self):
        (x3, y3, w, h) = self.get_allocation()
        def draw_tile_box(x, y):
            """
            Draws the slippy map tile x, y on the screen
            """
            
            key = (self.zoom_level,x,y)
            # Read tile from disk if not in memory cache
            if self.tiles.has_key(key):
                t = self.tiles[key]
            else:
                t = Tile(x, y, self.zoom_level)
                t.load()
                self.tiles[key] = t

            edges = tilenames.tileEdges(x, y, self.zoom_level)
            offsetlat = edges[2]-focus[0]  # North edge offset
            offsetlong = edges[1]-focus[1] # West edge offset
            self.tileheight_deg = edges[2]-edges[0]
            self.tilewidth_deg = edges[3]-edges[1]

            px = int(offsetlong / self.tilewidth_deg * 256)
            py = int(-offsetlat / self.tileheight_deg * 256)

            self.window.draw_pixbuf(self.get_style().fg_gc[gtk.STATE_NORMAL],
                    t.pixbuf, 0, 0, w/2 + int(px), h/2 + int(py) )
            
            """
            Adding placemark icons from the database and removing them when user is moving the map
            """      
            if (self.draw_icons == True):
                self.dbobjects = self.get_objects_from_db()
                
                
                #if (self.i % 20 == 0):
                for e in self.dbobjects:
                                        
                    
                    if e.__class__ == Mission:
                        (f,g) = self._coord_to_pixel(e.long,e.lat)
                        if (e.status != 3):
                            self.window.draw_pixbuf(self.get_style().fg_gc[gtk.STATE_NORMAL], self.mission_pic, 0, 0, int(f), int(g),24,24)
                    #if e.__class__ == Employee:
                        #self.window.draw_pixbuf(self.get_style().fg_gc[gtk.STATE_NORMAL], self.employee.pic, 0, 0, int(f), int(g),24,24)
                self.i = self.i-1  
            
            
        # Find x, y of tile in focus
        focus = self.focus
        x, y = tilenames.tileXY(focus[0], focus[1], self.zoom_level)

        # Cover screen with tiles by adding "safety margin" to all sides
        num_h = w/256+3
        off_x = num_h/2
        num_v = h/256+3
        off_y = num_v/2
        xtiles = range(x-off_x, x-off_x+num_h)
        ytiles = range(y-off_y, y-off_y+num_v)

        # Draw visible tiles
        for tx in xtiles:
            for ty in ytiles:
                draw_tile_box(tx,ty)

        # unload tiles not visible on screen from memory
        for key in self.tiles.keys():
            if not (key[1] in xtiles and key[2] in ytiles):
                del self.tiles[key]

    def _pixel_to_coord(self, dx, dy):
        """
        Converts pixel offset from map center (focus) to coordinates.
        """
        return (self.focus[0] - dy*self.tileheight_deg/256,
                dx*self.tilewidth_deg/256 + self.focus[1])
        
    def _coord_to_pixel(self, lon, lat):
        (x3, y3, w, h) = self.get_allocation()
        size_x = self.tilewidth_deg/256
        size_y = self.tileheight_deg/256
        
        coord_x_edge = self.focus[1] - size_x*(w/2)
        coord_y_edge = self.focus[0] + size_y*(h/2)
        
        return ((lon - coord_x_edge)/size_x,
                 (coord_y_edge - lat)/size_y)
        
    def get_objects_from_db(self):
        self.objectlist =[]
        for objectos in self.all_missions:
            
            self.objectlist.append(objectos)
        #for objectos in self.all_employees:
            
            #self.objectlist.append(objectos)
             
        return self.objectlist
    """
    Creates a popup with info database objects
    """
    
    def popupWindow(self):
        self.popup = gtk.Window(WINDOW_POPUP)
    
    def popup(self):                     
        self.objectlist2 = self.get_objects_from_db()
        
        
        
        dialog = gtk.AboutDialog()
        dialog.set_name(self.objectlist2[self.object_counter-1].title)
        dialog.set_comments("Radda kattjaveln i tradet")
        dialog.show()
        dialog.run()
        dialog.destroy()
        self.draw_icons = True
        

gobject.type_register(MapWidget)
gobject.signal_new("focus-changed", MapWidget, gobject.SIGNAL_RUN_FIRST, gobject.TYPE_NONE, (gobject.TYPE_PYOBJECT,))
gobject.signal_new("map-clicked", MapWidget, gobject.SIGNAL_RUN_FIRST, gobject.TYPE_NONE, (gobject.TYPE_PYOBJECT,))
