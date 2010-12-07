# -*- coding: utf-8 -*-
import gtk
import math
import time

class Map(gtk.DrawingArea):
    __bounds = {"min_latitude":0,
                "max_latitude":0,
                "min_longitude":0,
                "max_longitude":0}

    def __init__(self, map):
        gtk.DrawingArea.__init__(self)
        
        # Variabler
        self.__map = map
        self.__pos = {"x":0, "y":0}
        self.__origin_position = None
        self.__cols = 0
        self.__rows = 0
        self.__gps_data = None
        self.__movement_from = {"x": 0, "y":0}
        self.__allow_movement = False
        self.__last_movement_timestamp = 0.0
        self.__zoom_level = 1
        
        # queue_draw() ärvs från klassen gtk.DrawingArea
        map.set_redraw_function(self.queue_draw)
      
        self.connect("expose_event", self.handle_expose_event)
        self.connect("button_press_event", self.handle_button_press_event)
        self.connect("button_release_event", self.handle_button_release_event)
        self.connect("motion_notify_event", self.handle_motion_notify_event)
        self.set_events(gtk.gdk.BUTTON_PRESS_MASK |
                        gtk.gdk.BUTTON_RELEASE_MASK |
                        gtk.gdk.EXPOSURE_MASK |
                        gtk.gdk.LEAVE_NOTIFY_MASK |
                        gtk.gdk.POINTER_MOTION_MASK |
                        gtk.gdk.POINTER_MOTION_HINT_MASK)

    def change_zoom(self, change):
        # Frigör minnet genom att ladda ur alla tiles för föregående nivå
        level = self.__map.get_level(self.__zoom_level)
        level.unload_tiles("all")
      
        if change == "+":
            if self.__zoom_level < 3:
                self.__zoom_level += 1
        else:
            if self.__zoom_level > 1:
                self.__zoom_level -= 1

        # Ritar ny nivå
        self.queue_draw()

    # Hanterar rörelse av kartbilden
    def handle_button_press_event(self, widget, event):
        self.__movement_from["x"] = event.x
        self.__movement_from["y"] = event.y
        self.__origin_position = self.__map.get_focus()
        self.__last_movement_timestamp = time.time()
        self.__allow_movement = True

        return True

    def handle_button_release_event(self, widget, event):
        self.__allow_movement = False
        return True

    def handle_motion_notify_event(self, widget, event):
        if self.__allow_movement:
            if event.is_hint:
                x, y, state = event.window.get_pointer()
            else:
                x = event.x
                y = event.y
                state = event.state

            # Genom tidskontroll undviker vi oavsiktlig rörelse av kartan,
            # t ex ifall någon råkar nudda skärmen med ett finger eller liknande.
            if time.time() > self.__last_movement_timestamp + 0.1:
                lon, lat = self.pixel_to_gps(self.__movement_from["x"] - x,
                                             self.__movement_from["y"] - y)
                self.__map.set_focus(self.__origin_position["longitude"] + lon,
                                     self.__origin_position["latitude"] - lat)
                self.__movement_from["x"] = x
                self.__movement_from["y"] = y
            
                # Ritar om kartan
                self.queue_draw()

        return True

    def handle_expose_event(self, widget, event):
        self.context = widget.window.cairo_create()

        # Regionen vi ska rita på
        self.context.rectangle(event.area.x,
                               event.area.y,
                               event.area.width,
                               event.area.height)
        self.context.clip()
        self.draw()

        return False

    def set_gps_data(self, gps_data):
        self.__gps_data =  gps_data
        self.queue_draw()

    def draw(self):
        # Hämtar alla tiles för en nivå
        level = self.__map.get_level(self.__zoom_level)
        # Plockar ur de tiles vi söker från nivån
        tiles, cols, rows = level.get_tiles(self.__map.get_focus())
        self.__cols = cols
        self.__rows = rows

        self.__bounds["min_longitude"] = tiles[0].get_bounds()["min_longitude"]
        self.__bounds["min_latitude"] = tiles[0].get_bounds()["min_latitude"]
        self.__bounds["max_longitude"] = tiles[-1].get_bounds()["max_longitude"]
        self.__bounds["max_latitude"] = tiles[-1].get_bounds()["max_latitude"]

        # Ritar kartan
        for tile in tiles:
            #img = tile.get_picture()
            x, y = self.gps_to_pixel(tile.get_bounds()["min_longitude"],
                                     tile.get_bounds()["min_latitude"])
            tile.draw(self.context, x, y)

        # Ritar ut eventuella objekt
        objects = self.__map.get_objects()
        for item in objects:
            x, y = self.gps_to_pixel(item["object"].get_coordinate()["longitude"],
                                     item["object"].get_coordinate()["latitude"])

            if x != 0 and y != 0:
                item["object"].draw(self.context, x, y)
   
    def gps_to_pixel(self, lon, lat):
        cols = self.__cols
        rows = self.__rows
        width = self.__bounds["max_longitude"] - self.__bounds["min_longitude"]
        height = self.__bounds["min_latitude"] - self.__bounds["max_latitude"]
      
        # Ger i procent var vi befinner oss på width och height
        where_lon = (lon - self.__bounds["min_longitude"]) / width
        where_lat = (self.__bounds["min_latitude"] - lat) / height
      
        # Ger i procent var focus befinner sig på width och height
        where_focus_lon = (self.__map.get_focus()["longitude"] - \
                           self.__bounds["min_longitude"]) / width
        where_focus_lat = (self.__bounds["min_latitude"] - \
                           self.__map.get_focus()["latitude"]) / height
      
        # Placerar origo i skärmens centrum
        rect = self.get_allocation()
        x = rect.width / 2.0
        y = rect.height / 2.0
      
        # Räknar ut position:
        x += (where_lon - where_focus_lon) * (cols * 300.0)
        y += (where_lat - where_focus_lat) * (rows * 160.0)
      
        return [round(x), round(y)]
   
    def pixel_to_gps(self, movement_x, movement_y):
        # Hämtar alla tiles för en nivå
        level = self.__map.get_level(self.__zoom_level)
        # Plockar ur de tiles vi söker från nivån
        tiles, cols, rows = level.get_tiles(self.__map.get_focus())
      
        # Gps per pixlar
        width = self.__bounds["max_longitude"] - self.__bounds["min_longitude"]
        height = self.__bounds["min_latitude"] - self.__bounds["max_latitude"]
        gps_per_pix_width = width / (cols * 300)
        gps_per_pix_height = height / (rows * 160)
      
        # Observera att kartans GPS-koordinatsystem börjar i vänstra nedre
        # hörnet, medan cairo börjar i vänstra övre hörnet! På grund av detta
        # inverterar vi värdet vi räknar fram så båda koordinatsystemen
        # överensstämmer.
        return [gps_per_pix_width * movement_x,
                gps_per_pix_height * movement_y]
