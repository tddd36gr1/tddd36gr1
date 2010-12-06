# -*- coding: utf-8 -*-
import time
import gtk
import struct
import math

# Tar reda på en PNG-bilds storlek
def png_size(path):
    stream = open(path, "rb")

    # Dummy read to skip header data
    stream.read(12)
    if stream.read(4) == "IHDR":
        (x, y) = struct.unpack("!LL", stream.read(8))
        error = "no error"

    return (x, y, error)

# Ger en lista med snittet mellan två listor
def intersection(list1, list2):
    int_dict = {}
    list1_dict = {}

    for e in list1:
        list1_dict[e.get_name()] = e
    for e in list2:
        if list1_dict.has_key(e.get_name()):
            int_dict[e.get_name()] = e

    return int_dict.values()

# Ger en lista med unionen mellan två listor
def union(list1, list2):
    union_dict = {}
    for e in list1:
        union_dict[e.get_name()] = e
    for e in list2:
        union_dict[e.get_name()] = e

    return union_dict.values()

class Name:
    __name = None

    def __init__(self):
        pass

    def set_name(self, name):
        self.__name = name

    def get_name(self):
        return self.__name

class Picture:
    __path_to_picture = None
    __picture = None
    __commands = None

    def set_path_to_picture(self, path):
        self.__path_to_picture = path

    def get_path_to_picture(self):
        return self.__path_to_picture

    def draw_shapes(self, context, x, y, commands):
        for cmd in commands:
            eval('context.'+cmd)
        context.stroke()

    def draw_picture(self, context, x, y):
        context.set_source_pixbuf(self.get_picture(), x, y)
        context.paint()

    def draw(self, context, x, y):
        if self.get_path_to_picture():
            self.draw_picture(context, x, y)
        else:
            self.draw_shapes(context, x, y, self.get_commands())

    def set_commands(self, commands):
        self.__commands = commands

    def get_commands(self):
        return self.__commands

    def load_picture(self):
        self.__picture = gtk.gdk.pixbuf_new_from_file(self.get_path_to_picture())

    def unload_picture(self):
        self.__picture = None        

    def get_picture(self):
        if self.__picture:
            return self.__picture
        else:
            self.load_picture()
            return self.__picture

class Bounds:
    __bounds = None

    def set_bounds(self, bounds):
        self.__bounds = bounds

    def get_bounds(self):
        return self.__bounds

# Lagrar en kartbild och dess koordinatavgränsningar
class MapTile(Picture, Bounds, Name):
    __type = None

    def set_type(self, type):
        self.__type = type

    def get_type(self):
        return self.__type

    def __init__(self, id, path, bounds, type):
        self.set_name(id)
        self.set_path_to_picture(path)
        self.set_bounds(bounds)
        self.set_type(type)

# Lagrar alla MapTiles (kartbilder)
class Tiles:
    # Håller reda på vilket område samtliga tiles omfattar
    __bounds = {"min_latitude":None,
                "max_latitude":None,
                "min_longitude":None,
                "max_longitude":None}

    # Lagrar alla tiles
    __tiles = None

    def get_cols(self):
        return self.__cols

    def get_rows(self):
        return self.__rows

    def __init__(self, width, height):
        # Lagrar basbildens bredd och höjd
        self.__width = int(width)
        self.__height = int(height)
        
        # Behövs för att lägga in tiles
        self.__col_pos = 0
        self.__row_pos = 0
    
        # Behövs för matematiska beräkningar
        self.__cols = 0
        self.__rows = 0

    def update_bounds(self, bounds):
        if self.__bounds["min_latitude"] == None:
            self.__bounds["min_latitude"] = bounds["min_latitude"]
        elif bounds["min_latitude"] > self.__bounds["min_latitude"]:
            self.__bounds["min_latitude"] = bounds["min_latitude"]

        if self.__bounds["max_latitude"] == None:
            self.__bounds["max_latitude"] = bounds["max_latitude"]
        elif bounds["max_latitude"] < self.__bounds["max_latitude"]:
            self.__bounds["max_latitude"] = bounds["max_latitude"]

        if self.__bounds["min_longitude"] == None:
            self.__bounds["min_longitude"] = bounds["min_longitude"]
        elif bounds["min_longitude"] < self.__bounds["min_longitude"]:
            self.__bounds["min_longitude"] = bounds["min_longitude"]

        if self.__bounds["max_longitude"] == None:
            self.__bounds["max_longitude"] = bounds["max_longitude"]
        elif bounds["max_longitude"] > self.__bounds["max_longitude"]:
            self.__bounds["max_longitude"] = bounds["max_longitude"]

    def create_empty_tiles(self, cols, rows):
        self.__cols = cols
        self.__rows = rows
        self.__tiles = [[[] for ni in range(rows)] for mi in range(cols)]

    def get_bounds(self):
        return self.__bounds

    def add_tile(self, tile):
        self.update_bounds(tile.get_bounds())
        self.__tiles[self.__col_pos][self.__row_pos] = tile

        if tile.get_type() == "end":
            self.__row_pos += 1
            self.__col_pos = 0
        else:
            self.__col_pos += 1

    # Laddar ur tiles för att frigöra minnet
    def unload_tiles(self, tiles_list):
        if tiles_list == "all":
            tiles_list = self.__tiles

        for tiles in tiles_list:
            for tile in tiles:
                tile.unload_picture()

    # Hämtar alla tiles som ligger inom ett avgränsat koordinatområde
    # Kom ihåg att latitude växer från botten mot toppen, inte tvärtom. Dock
    # kallas topppen för min_latitude.
    def get_tiles(self, focus):
        gps_width = self.__bounds["max_longitude"] - \
                    self.__bounds["min_longitude"]
        gps_height = self.__bounds["min_latitude"] - \
                     self.__bounds["max_latitude"]

        # Skärmen på N810:an är 800x480.
        width = (gps_width / self.__width) * 400
        height = (gps_height / self.__height) * 240

        bounds = {"min_longitude":(focus["longitude"] - width),
                  "max_longitude":(focus["longitude"] + width),
                  "min_latitude":focus["latitude"] + height,
                  "max_latitude":focus["latitude"] - height}

        # Undviker att vi hamnar utanför det område tiles:en täcker
        if bounds["min_longitude"] < self.__bounds["min_longitude"]:
            bounds["min_longitude"] = self.__bounds["min_longitude"]

        if bounds["max_longitude"] > self.__bounds["max_longitude"]:
            bounds["max_longitude"] = self.__bounds["max_longitude"]

        if bounds["min_latitude"] > self.__bounds["min_latitude"]:
            bounds["min_latitude"] = self.__bounds["min_latitude"]

        if bounds["max_latitude"] < self.__bounds["max_latitude"]:
            bounds["max_latitude"] = self.__bounds["max_latitude"]

        start_lon = bounds["min_longitude"] - self.__bounds["min_longitude"]
        stop_lon = bounds["max_longitude"] - self.__bounds["min_longitude"]
        start_lat = self.__bounds["min_latitude"] - bounds["min_latitude"]
        stop_lat = self.__bounds["min_latitude"] - bounds["max_latitude"]

        # Det bästa sättet att förstå matematiken nedanför är att rita upp ett
        # rutnät med alla tiles, dvs x * y, t ex 3x5. Börja sedan räkna på
        # matematiken nedan utifrån rutnätet. I enkelhet handlar det nedan
        # om att räkna ut i procent var vi befinner oss i x-led och y-led
        # och sedan gångra denna procent med antalet kolumner och rader vi har,
        # och på så vis få reda på vilka rutor som ska visas.
        # Algoritmen är inte på något vis perfekt och bättre lösningar finns
        # säkert.
        x_start = int(math.floor(self.__cols * (start_lon / gps_width)))
        x_stop = int(math.ceil(self.__cols * (stop_lon / gps_width)))
        if x_stop == self.__cols:
            x_stop -= 1 # Så vi inte överskrider max antalet tiles i x-led.

        y_start = int(math.floor(self.__rows * (start_lat / gps_height)))
        y_stop = int(math.ceil(self.__rows * (stop_lat / gps_height)))
        if y_stop == self.__rows:
            y_stop -= 1 # Så vi inte överskrider max antalet tiles i y-led.

        # Frigör minne genom att ladda ur de tiles som inte visas
        tiles_left = []
        if x_start - 1 >= 0:
            self.unload_tiles(self.__tiles[0:x_start])

        tiles_right = []
        if x_stop + 1 != self.__cols:
            self.unload_tiles(self.__tiles[x_stop:self.__cols])

        # Returnerar de tiles som efterfrågas
        tiles = self.__tiles[x_start:x_stop + 1]
        result = []
        for tile in tiles:
            result += tile[y_start:y_stop + 1]

        return [result,
                x_stop + 1 - x_start,
                y_stop + 1 - y_start]

# Datastruktur som lagrar kartans bild och de generella objekt som ska ritas ut
# på denna. Med generella objekt menas objekt som hela tiden ska vara på kartan,
# som ej försvinner när exempelvis ett uppdrag avslutats.
class MapData(Bounds, Name):
    __objects = []
    __mission_objects = []
    __levels = {}
    __redraw_function = None
    __focus = {"latitude":0,
               "longitude":0}

    # name är namnet på kartan, t ex Ryd.
    # levels är tre stycken Tiles-objekt.
    def __init__(self, name, levels):
        self.set_name(name)
        self.set_level(1, levels[1])
        self.set_level(2, levels[2])
        self.set_level(3, levels[3])
        self.set_bounds(levels[1].get_bounds())

    # Ställer in Tiles-objekt för en bestämd nivå
    def set_level(self, level, tiles):
        self.__levels[level] = tiles

    # Returnerar ett Tiles-objekt för en given nivå
    def get_level(self, level):
        return self.__levels[level]

    def set_focus(self, longitude, latitude):
        self.__focus["longitude"] = longitude
        self.__focus["latitude"] = latitude
        self.redraw()

    def get_focus(self):
        return self.__focus

    def remove_objects(self):
        self.__objects = []

    def add_object(self, object_id, map_object):
        self.__objects.append({"id":object_id,
                               "object":map_object})

    def delete_object(self, object_id):
        for item in self.__objects:
            if item["id"] == object_id:
                self.__objects.remove(item)

    def get_object(self, object_id):
        for item in self.__objects:
            if item["id"] == object_id:
                return self.__objects[item]

    def get_objects(self):
        return self.__objects

    def set_redraw_function(self, redraw_function):
        self.__redraw_function = redraw_function

    def redraw(self):
        if self.__redraw_function:
            self.__redraw_function()

# Är den typen av objekt som lagras i MapData. T ex en ambulans som ska visas
# på kartan eller "blockerad väg"-symbol.
class MapObject(Picture, Name):
    __coordinate = None

    # coordinate-variabeln är en dict enligt
    # {"latitude":float, "longitude":float}
    # type är objektets typ, anges med siffra. Kan vara en ambulans, polisbil,
    # ett träd eller vad man nu hittar på.
    def __init__(self, coordinate, *path):
        self.set_coordinate(coordinate)
        if len(path) == 1:
            self.set_path_to_picture(*path)
        else:
            self.set_commands(path)

    def set_coordinate(self, coordinate):
        self.__coordinate = coordinate

    def get_coordinate(self):
        return self.__coordinate

    def set_visible(self, visible):
        self.__visible = visible

    def get_visible(self):
        return self.__visible
